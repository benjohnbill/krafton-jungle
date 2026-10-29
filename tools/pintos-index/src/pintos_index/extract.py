"""libclang walk over the kernel set into Symbols, Edges, and value-flow stores.

Function pointers are tracked as values flowing into sinks. A sink is a struct
field, a variable (global, static, local, or array), or a function parameter.
Every store of a function into a sink becomes a `registers` edge, and every
indirect call resolves its candidates by following the sinks its callee
expression reads (FINAL C2, C15).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from clang import cindex as ci

from . import clangloc as L
from .model import Edge, Param, Symbol

K = ci.CursorKind
EXTRA_FLAG = "-Wno-error=int-conversion"
WRAPPERS = {K.UNEXPOSED_EXPR, K.PAREN_EXPR, K.CSTYLE_CAST_EXPR, K.UNARY_OPERATOR}
RECORDS = {K.STRUCT_DECL, K.UNION_DECL}
ASSIGN_OPS = {"=", "*=", "/=", "%=", "+=", "-=", "<<=", ">>=", "&=", "^=", "|="}


def compile_args(entry: dict) -> list[str]:
    raw = entry["arguments"][1:]
    out, skip = [], False
    for a in raw:
        if skip:
            skip = False
            continue
        if a == "-o":
            skip = True
            continue
        if a == "-c" or a == entry["file"]:
            continue
        out.append(a)
    return out + [EXTRA_FLAG]


def is_fnptr(t: ci.Type) -> bool:
    t = t.get_canonical()
    while t.kind in (ci.TypeKind.CONSTANTARRAY, ci.TypeKind.INCOMPLETEARRAY):
        t = t.element_type.get_canonical()
    return t.kind == ci.TypeKind.POINTER and t.get_pointee().get_canonical().kind in (
        ci.TypeKind.FUNCTIONPROTO,
        ci.TypeKind.FUNCTIONNOPROTO,
    )


def fn_type_of(t: ci.Type) -> str:
    t = t.get_canonical()
    if t.kind == ci.TypeKind.POINTER:
        t = t.get_pointee().get_canonical()
    return t.spelling


def as_init_list(c: ci.Cursor) -> ci.Cursor | None:
    c = unwrap(c)
    if c.kind == K.COMPOUND_LITERAL_EXPR:
        c = next((k for k in c.get_children() if k.kind == K.INIT_LIST_EXPR), c)
    return c if c.kind == K.INIT_LIST_EXPR else None


def unwrap(c: ci.Cursor) -> ci.Cursor:
    while c.kind in WRAPPERS:
        kids = list(c.get_children())
        if not kids:
            return c
        if c.kind == K.UNEXPOSED_EXPR and kids[0].kind == K.MEMBER_REF:
            return c
        c = kids[-1]
    return c


@dataclass
class VarInfo:
    name: str
    local: bool
    fn: str | None


@dataclass
class Store:
    value: tuple
    ev: str
    col: int
    fn: str | None


@dataclass
class DispatchSite:
    src: str
    callee: tuple
    fn_type: str
    ev: str
    col: int
    via_macro: str | None


@dataclass
class Facts:
    symbols: dict[str, Symbol] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)
    refs: list[dict] = field(default_factory=list)
    stores: dict[tuple, list[Store]] = field(default_factory=dict)
    sink_names: dict[tuple, str] = field(default_factory=dict)
    vars: dict[str, VarInfo] = field(default_factory=dict)
    dispatch_sites: list[DispatchSite] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    files_read: set[str] = field(default_factory=set)
    macros: dict[str, Symbol] = field(default_factory=dict)
    instantiations: dict[tuple, tuple] = field(default_factory=dict)
    fn_extents: dict[str, list[tuple[int, int, str]]] = field(default_factory=dict)
    fn_types: dict[str, str] = field(default_factory=dict)
    decl_type_refs: dict[str, list[Edge]] = field(default_factory=dict)


class Walker:
    def __init__(self, root: Path):
        self.root = str(root.resolve())
        self.facts = Facts()
        self._seen_top: set[tuple] = set()
        self._seen_inc: set[tuple] = set()
        self._text: dict[str, bytes] = {}
        self._macro_at: dict[tuple, str] = {}
        self._container_var: str | None = None

    def at(self, loc: ci.SourceLocation) -> tuple[str | None, int, int, int]:
        name, line, col, off = L.file_loc(loc)
        return L.rel(self.root, name), line, col, off

    def ev(self, c: ci.Cursor) -> tuple[str, int]:
        f, line, col, _ = self.at(c.location)
        return f"{f}:{line}", col

    def text(self, c: ci.Cursor) -> str:
        macro = self.via_macro(c) if c.kind.is_expression() else None
        if macro:
            toks = " ".join(t.spelling for t in c.get_tokens())
            inner = unwrap(c)
            if toks:
                return toks
            if inner.kind == K.DECL_REF_EXPR:
                return inner.spelling
            return f"(expression inside macro {macro})"
        f1, _, _, o1 = self.at(c.extent.start)
        f2, _, _, o2 = self.at(c.extent.end)
        if f1 is None or f1 != f2 or o2 < o1:
            return " ".join(t.spelling for t in c.get_tokens())
        if f1 not in self._text:
            self._text[f1] = (Path(self.root) / f1).read_bytes()
        return " ".join(self._text[f1][o1:o2].decode(errors="replace").split())

    def via_macro(self, c: ci.Cursor) -> str | None:
        """Name of the macro whose body produced c, or None for code the user wrote.

        A macro body token's file location is the macro name's expansion
        location; a macro argument token keeps its own position.
        """
        if c.location.file is None:
            return None
        key = (L.rel(self.root, c.location.file.name), c.location.line, c.location.column)
        f, line, col, _ = self.at(c.location)
        if (f, line, col) != key:
            return None
        return self._macro_at.get(key)

    def parse(self, index: ci.Index, entry: dict) -> None:
        os.chdir(entry["directory"])
        tu = index.parse(
            entry["file"],
            args=compile_args(entry),
            options=ci.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD,
        )
        for d in tu.diagnostics:
            if d.severity >= ci.Diagnostic.Error:
                f = L.rel(self.root, d.location.file.name if d.location.file else None)
                self.facts.errors.append(f"{f}:{d.location.line}: {d.spelling}")
        main = L.rel(self.root, tu.spelling)
        self.facts.files_read.add(main)
        for inc in tu.get_includes():
            src = L.rel(self.root, inc.source.name)
            dst = L.rel(self.root, inc.include.name)
            self.facts.files_read.add(dst)
            key = (src, inc.location.line)
            if src and dst and key not in self._seen_inc:
                self._seen_inc.add(key)
                self.facts.edges.append(
                    Edge("includes", f"file:{src}", f"{src}:{inc.location.line}", f"file:{dst}", col=inc.location.column)
                )
        tops = list(tu.cursor.get_children())
        self._macro_at = {}
        for c in tops:
            if c.kind == K.MACRO_INSTANTIATION and c.location.file:
                f = L.rel(self.root, c.location.file.name)
                self._macro_at[(f, c.location.line, c.location.column)] = c.spelling
        for c in tops:
            f = L.rel(self.root, c.location.file.name) if c.location.file else None
            if f is None:
                continue
            key = (f, c.extent.start.offset, c.kind)
            if key in self._seen_top:
                continue
            self._seen_top.add(key)
            self.top(c, f)

    def top(self, c: ci.Cursor, f: str) -> None:
        if c.kind == K.FUNCTION_DECL:
            self.function(c)
        elif c.kind in RECORDS and c.is_definition():
            self.record(c, None)
        elif c.kind == K.TYPEDEF_DECL:
            self.typedef(c)
            for child in c.get_children():
                if child.kind in RECORDS and child.is_definition():
                    self.record(child, None)
        elif c.kind == K.VAR_DECL:
            self.var_info(c)
            self._container_var = c.spelling
            self.visit(c, None, [])
            self._container_var = None
        elif c.kind == K.MACRO_DEFINITION and L.is_function_like_macro(c):
            self.facts.macros[c.get_usr()] = Symbol(
                c.get_usr(), c.spelling, "macro", f, c.location.line, "#define " + self.text(c), None
            )
        elif c.kind == K.MACRO_INSTANTIATION:
            ref = c.referenced
            if ref is not None and L.is_function_like_macro(ref):
                self.facts.instantiations[(f, c.extent.start.offset)] = (ref.get_usr(), c.location.line, c.location.column)

    def function(self, c: ci.Cursor) -> None:
        usr = c.get_usr()
        f, line, _, _ = self.at(c.location)
        self.facts.fn_types[usr] = c.type.get_canonical().spelling
        sym = self.facts.symbols.get(usr)
        body = next((k for k in c.get_children() if k.kind == K.COMPOUND_STMT), None)
        if body is None:
            if sym is None:
                self.facts.symbols[usr] = Symbol(
                    usr, c.spelling, "function", f, line, self.text(c), c.raw_comment, defined=False,
                    return_type=c.result_type.spelling,
                    params=[Param(a.spelling, a.type.spelling) for a in c.get_arguments()],
                )
            elif sym.comment is None:
                sym.comment = c.raw_comment
            if usr not in self.facts.decl_type_refs:
                self.facts.decl_type_refs[usr] = []
                self.type_refs(c, usr, self.facts.decl_type_refs[usr])
            return
        f1, _, _, o1 = self.at(c.extent.start)
        _, _, _, o2 = self.at(body.extent.start)
        if f1 not in self._text:
            self._text[f1] = (Path(self.root) / f1).read_bytes()
        signature = " ".join(self._text[f1][o1:o2].decode(errors="replace").split())
        comment = c.raw_comment or (sym.comment if sym else None)
        self.facts.symbols[usr] = Symbol(
            usr, c.spelling, "function", f, line, signature, comment, defined=True,
            return_type=c.result_type.spelling,
            params=[Param(a.spelling, a.type.spelling) for a in c.get_arguments()],
        )
        _, _, _, end = self.at(c.extent.end)
        self.facts.fn_extents.setdefault(f1, []).append((o1, end, usr))
        self.type_refs(c, usr, self.facts.edges)
        self.visit(body, usr, [])

    def type_refs(self, c: ci.Cursor, usr: str, sink: list[Edge]) -> None:
        types = [(c.result_type, c)] + [(a.type, a) for a in c.get_arguments()]
        seen = set()
        for t, at in types:
            self.type_ref(usr, t, at, sink, seen)

    def type_ref(self, src: str, t: ci.Type, at: ci.Cursor, sink: list[Edge] | None = None, seen: set | None = None) -> None:
        while True:
            t2 = t
            if t.kind == ci.TypeKind.POINTER:
                t = t.get_pointee()
            elif t.kind in (ci.TypeKind.CONSTANTARRAY, ci.TypeKind.INCOMPLETEARRAY):
                t = t.element_type
            if t2 is t:
                break
        d = t.get_declaration()
        if d.kind not in RECORDS and d.kind != K.TYPEDEF_DECL:
            return
        f = L.rel(self.root, d.location.file.name) if d.location.file else None
        if f is None:
            return
        ev, col = self.ev(at)
        key = d.get_usr()
        if not key or key == src or (seen is not None and key in seen):
            return
        if seen is not None:
            seen.add(key)
        (self.facts.edges if sink is None else sink).append(Edge("refs_type", src, ev, key, col=col))

    def record(self, c: ci.Cursor, owner: str | None) -> None:
        anon_member = c.is_anonymous() and owner is not None
        usr = owner if anon_member else c.get_usr()
        if not anon_member:
            f, line, _, _ = self.at(c.location)
            kw = "union" if c.kind == K.UNION_DECL else "struct"
            name = c.spelling if not c.is_anonymous() else c.type.spelling
            self.facts.symbols.setdefault(
                usr, Symbol(usr, name, "struct", f, line, f"{kw} {name}", c.raw_comment)
            )
        for k in c.get_children():
            if k.kind == K.FIELD_DECL:
                if not k.spelling:
                    continue
                f, line, _, _ = self.at(k.location)
                ku = k.get_usr()
                self.facts.symbols[ku] = Symbol(ku, k.spelling, "field", f, line, self.text(k), k.raw_comment)
                attrs = {"anonymous": True} if anon_member else {}
                self.facts.edges.append(Edge("field_of", ku, f"{f}:{line}", usr, col=k.location.column, attrs=attrs))
                self.type_ref(ku, k.type, k)
                self.visit(k, None, [])
            elif k.kind in RECORDS and k.is_definition():
                self.record(k, usr if k.is_anonymous() else None)

    def typedef(self, c: ci.Cursor) -> None:
        usr = c.get_usr()
        f, line, _, _ = self.at(c.location)
        self.facts.symbols[usr] = Symbol(usr, c.spelling, "typedef", f, line, self.text(c), c.raw_comment)
        self.type_ref(usr, c.underlying_typedef_type, c)

    def var_info(self, c: ci.Cursor) -> None:
        local = c.semantic_parent is not None and c.semantic_parent.kind == K.FUNCTION_DECL
        self.facts.vars[c.get_usr()] = VarInfo(c.spelling, local, c.semantic_parent.get_usr() if local else None)

    def param_index(self, p: ci.Cursor) -> tuple[str, int]:
        fn = p.semantic_parent
        for i, a in enumerate(fn.get_arguments()):
            if a.spelling == p.spelling:
                return fn.get_usr(), i
        return fn.get_usr(), -1

    def value(self, e: ci.Cursor) -> tuple:
        e = unwrap(e)
        k = e.kind
        if k == K.DECL_REF_EXPR:
            r = e.referenced
            if r is None:
                return ("opaque",)
            if r.kind == K.FUNCTION_DECL:
                ev, col = self.ev(e)
                return ("func", r.get_usr(), ev, col)
            if r.kind == K.VAR_DECL:
                return ("var", r.get_usr())
            if r.kind == K.PARM_DECL:
                return ("param", *self.param_index(r))
            return ("null",)
        if k == K.MEMBER_REF_EXPR and e.referenced is not None:
            return ("field", e.referenced.get_usr())
        if k == K.ARRAY_SUBSCRIPT_EXPR:
            return self.value(next(e.get_children()))
        if k == K.CONDITIONAL_OPERATOR:
            kids = list(e.get_children())
            return ("multi", [self.value(kids[1]), self.value(kids[2])])
        if k in (K.INTEGER_LITERAL, K.CXX_NULL_PTR_LITERAL_EXPR):
            return ("null",)
        return ("opaque",)

    def sink(self, lhs: ci.Cursor) -> tuple | None:
        v = self.value(lhs)
        return v if v[0] in ("var", "field", "param") else None

    def sink_name(self, s: tuple, c: ci.Cursor) -> None:
        if s in self.facts.sink_names:
            return
        if s[0] == "field":
            r = c.referenced
            parent = r.semantic_parent
            while parent is not None and parent.is_anonymous() and parent.semantic_parent.kind in RECORDS:
                parent = parent.semantic_parent
            self.facts.sink_names[s] = f"field {parent.spelling if parent else '?'}.{r.spelling}"
        elif s[0] == "var":
            v = self.facts.vars.get(s[1])
            self.facts.sink_names[s] = f"{'local' if v and v.local else 'global'} {v.name if v else '?'}"
        else:
            sym_fn = c.referenced.semantic_parent if c.referenced is not None and c.referenced.kind == K.PARM_DECL else None
            self.facts.sink_names[s] = f"param {s[2]} of {sym_fn.spelling if sym_fn else '?'}"

    def store(self, s: tuple | None, val: tuple, at: ci.Cursor, fn: str | None, typed: bool) -> None:
        if s is None or not (typed or _has_func(val)):
            return
        ev, col = self.ev(at)
        self.facts.stores.setdefault(s, []).append(Store(val, ev, col, fn))
        for fv in _funcs(val):
            self.facts.edges.append(
                Edge("registers", fn or f"file:{ev.rsplit(':', 1)[0]}", fv[2], fv[1], col=fv[3],
                     attrs={"into": self.facts.sink_names.get(s, str(s))})
            )

    def init_list(self, base: tuple | None, il: ci.Cursor, fn: str | None) -> None:
        t = il.type.get_canonical()
        kids = list(il.get_children())
        if t.kind == ci.TypeKind.RECORD:
            fields = [k for k in t.get_declaration().get_children() if k.kind == K.FIELD_DECL]
            pos = 0
            for k in kids:
                target, val = None, k
                if k.kind == K.UNEXPOSED_EXPR:
                    parts = list(k.get_children())
                    refs = [p for p in parts if p.kind == K.MEMBER_REF]
                    if refs:
                        target, val = refs[-1].referenced, parts[-1]
                        names = [f.spelling for f in fields]
                        pos = names.index(target.spelling) + 1 if target.spelling in names else pos
                if target is None:
                    if pos >= len(fields):
                        continue
                    target = fields[pos]
                    pos += 1
                s = ("field", target.get_usr())
                if s not in self.facts.sink_names:
                    owner = target.semantic_parent
                    self.facts.sink_names[s] = f"field {owner.spelling if owner else '?'}.{target.spelling}"
                inner = as_init_list(val)
                if inner is not None:
                    self.init_list(s, inner, fn)
                else:
                    self.store(s, self.value(val), val, fn, is_fnptr(target.type))
        else:
            for k in kids:
                inner = as_init_list(k)
                if inner is not None:
                    self.init_list(base, inner, fn)
                elif base is not None:
                    self.store(base, self.value(k), k, fn, is_fnptr(il.type))

    def param_root(self, e: ci.Cursor, fn: str) -> tuple[str | None, bool]:
        chain = False
        while True:
            if e.kind in WRAPPERS or e.kind in (K.MEMBER_REF_EXPR, K.ARRAY_SUBSCRIPT_EXPR):
                kids = list(e.get_children())
                if not kids:
                    return None, chain
                if e.kind in (K.MEMBER_REF_EXPR, K.ARRAY_SUBSCRIPT_EXPR):
                    chain = True
                    e = kids[0]
                else:
                    e = kids[-1] if e.kind != K.UNEXPOSED_EXPR else kids[0]
                continue
            break
        if e.kind == K.DECL_REF_EXPR and e.referenced is not None and e.referenced.kind == K.PARM_DECL:
            if e.referenced.semantic_parent.get_usr() == fn:
                return e.referenced.spelling, chain
        return None, chain

    def param(self, fn: str, name: str) -> Param | None:
        sym = self.facts.symbols.get(fn)
        return next((p for p in sym.params if p.name == name), None) if sym else None

    def visit(self, c: ci.Cursor, fn: str | None, parents: list[ci.Cursor], callee: bool = False) -> None:
        """Walks c. `callee` is True while c sits on the callee path of a CALL_EXPR."""
        k = c.kind
        if k == K.CALL_EXPR:
            self.call(c, fn)
        elif k == K.DECL_REF_EXPR and _in_source(c.referenced):
            f, line, col, _ = self.at(c.location)
            ctx = "call" if callee else "other"
            self.facts.refs.append({"usr": c.referenced.get_usr(), "at": f"{f}:{line}:{col}", "ctx": ctx, "in": fn, "in_var": self._container_var})
        elif k == K.BINARY_OPERATOR:
            op = L.binary_op(c)
            if op in ASSIGN_OPS:
                lhs, rhs = list(c.get_children())
                if op == "=":
                    s = self.sink(lhs)
                    if s:
                        self.sink_name(s, unwrap(lhs) if unwrap(lhs).kind != K.ARRAY_SUBSCRIPT_EXPR else unwrap(next(unwrap(lhs).get_children())))
                    self.store(s, self.value(rhs), rhs, fn, is_fnptr(lhs.type))
                if fn:
                    self.param_write(lhs, c, fn)
        elif k == K.UNARY_OPERATOR and fn:
            toks = [t.spelling for t in c.get_tokens()]
            if toks and (toks[0] in ("++", "--") or toks[-1] in ("++", "--")):
                self.param_write(next(c.get_children()), c, fn)
        elif k == K.VAR_DECL:
            if fn:
                self.var_info(c)
            init = [x for x in c.get_children() if x.kind not in (K.TYPE_REF, K.ANNOTATE_ATTR) and x.kind.is_expression()]
            if init:
                s = ("var", c.get_usr())
                v = self.facts.vars[c.get_usr()]
                self.facts.sink_names.setdefault(s, f"{'local' if v.local else 'global'} {v.name}")
                inner = as_init_list(init[-1])
                if inner is not None:
                    self.init_list(s, inner, fn)
                else:
                    self.store(s, self.value(init[-1]), init[-1], fn, is_fnptr(c.type))
        elif k == K.INIT_LIST_EXPR and not _nested_init(parents):
            self.init_list(None, c, fn)
        elif k == K.RETURN_STMT and fn:
            ev, _ = self.ev(c)
            kids = list(c.get_children())
            self.facts.symbols[fn].returns.append({"ev": ev, "expr": self.text(kids[0]) if kids else ""})
        parents.append(c)
        for i, child in enumerate(c.get_children()):
            on_path = (k == K.CALL_EXPR and i == 0) or (callee and k in WRAPPERS)
            self.visit(child, fn, parents, on_path)
        parents.pop()

    def param_write(self, lhs: ci.Cursor, at: ci.Cursor, fn: str) -> None:
        name, chain = self.param_root(lhs, fn)
        p = self.param(fn, name) if name else None
        if p is None:
            return
        ev, _ = self.ev(at)
        if chain:
            p.member_writes.append({"lhs": self.text(lhs), "ev": ev})
        else:
            p.writes.append(ev)

    def call(self, c: ci.Cursor, fn: str | None) -> None:
        kids = list(c.get_children())
        if not kids:
            return
        callee_expr = kids[0]
        callee = unwrap(callee_expr)
        args = list(c.get_arguments())
        arg_text = [self.text(a) for a in args]
        direct = callee.kind == K.DECL_REF_EXPR and _in_source(callee.referenced)
        if direct:
            target = callee.referenced
            dst = target.get_usr()
            ev, col = self.ev(callee)
            attrs = {"args": arg_text}
            vm = self.via_macro(callee)
            if vm:
                attrs["via_macro"] = vm
            if fn:
                self.facts.edges.append(Edge("calls", fn, ev, dst, col=col, attrs=attrs))
            params = list(target.get_arguments())
            for i, a in enumerate(args):
                ptype_fn = i < len(params) and is_fnptr(params[i].type)
                s = ("param", dst, i)
                self.facts.sink_names.setdefault(s, f"param {i} of {target.spelling}")
                self.store(s, self.value(a), a, fn, ptype_fn)
            callee_name = target.spelling
        else:
            ev, col = self.ev(callee if callee.kind == K.MEMBER_REF_EXPR else callee_expr)
            value = self.value(callee_expr)
            if fn:
                self.facts.dispatch_sites.append(
                    DispatchSite(fn, value, fn_type_of(callee_expr.type), ev, col, self.via_macro(callee))
                )
                s = value if value[0] in ("var", "field", "param") else None
                if s:
                    self.sink_name(s, callee if callee.kind != K.ARRAY_SUBSCRIPT_EXPR else unwrap(next(callee.get_children())))
            via = self.facts.sink_names.get(value) if value[0] in ("var", "field", "param") else None
            callee_name = f"indirect through {via}" if via else self.text(callee_expr)
        if fn:
            for i, a in enumerate(args):
                name, _ = self.param_root(a, fn)
                p = self.param(fn, name) if name else None
                if p is not None:
                    ev2, _ = self.ev(a)
                    p.passed_to.append({"callee": callee_name, "arg": i, "expr": arg_text[i], "ev": ev2})


def _in_source(d: ci.Cursor | None) -> bool:
    return d is not None and d.kind == K.FUNCTION_DECL


def _funcs(v: tuple) -> list[tuple]:
    if v[0] == "func":
        return [v]
    if v[0] == "multi":
        return [x for sub in v[1] for x in _funcs(sub)]
    return []


def _has_func(v: tuple) -> bool:
    return bool(_funcs(v))


def _nested_init(parents: list[ci.Cursor]) -> bool:
    """True when an enclosing init list or variable initializer already handled this list."""
    for p in reversed(parents):
        if p.kind in (K.INIT_LIST_EXPR, K.VAR_DECL):
            return True
        if p.kind not in WRAPPERS and p.kind != K.COMPOUND_LITERAL_EXPR:
            return False
    return False
