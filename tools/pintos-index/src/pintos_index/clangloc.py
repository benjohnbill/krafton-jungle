"""Source locations the Python bindings do not expose.

`cursor.location` is the expansion location. A call written inside a macro
argument then reports the macro name's column, while clang's file location
(and clangd) report the token the user wrote. These helpers return the file
location and the spelling location so the two cases stay apart.
"""

from __future__ import annotations

import ctypes
import os

from clang import cindex as ci

_lib = ci.conf.lib
_ARGS = [ci.SourceLocation, ctypes.POINTER(ci.c_object_p)] + [ctypes.POINTER(ctypes.c_uint)] * 3
for _name in ("clang_getFileLocation", "clang_getSpellingLocation"):
    getattr(_lib, _name).argtypes = _ARGS
    getattr(_lib, _name).restype = None
_lib.clang_Cursor_isMacroFunctionLike.argtypes = [ci.Cursor]
_lib.clang_Cursor_isMacroFunctionLike.restype = ctypes.c_uint
_lib.clang_getCursorBinaryOperatorKind.argtypes = [ci.Cursor]
_lib.clang_getCursorBinaryOperatorKind.restype = ctypes.c_int
_lib.clang_getBinaryOperatorKindSpelling.argtypes = [ctypes.c_int]
_lib.clang_getBinaryOperatorKindSpelling.restype = ci._CXString
_lib.clang_getBinaryOperatorKindSpelling.errcheck = ci._CXString.from_result
_lib.clang_getClangVersion.restype = ci._CXString
_lib.clang_getClangVersion.errcheck = ci._CXString.from_result


def _decode(fn, loc: ci.SourceLocation) -> tuple[str | None, int, int, int]:
    f = ci.c_object_p()
    line, col, off = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
    fn(loc, ctypes.byref(f), ctypes.byref(line), ctypes.byref(col), ctypes.byref(off))
    name = ci.File(f).name if f else None
    return name, line.value, col.value, off.value


def file_loc(loc: ci.SourceLocation) -> tuple[str | None, int, int, int]:
    return _decode(_lib.clang_getFileLocation, loc)


def spelling_loc(loc: ci.SourceLocation) -> tuple[str | None, int, int, int]:
    return _decode(_lib.clang_getSpellingLocation, loc)


def is_function_like_macro(c: ci.Cursor) -> bool:
    return bool(_lib.clang_Cursor_isMacroFunctionLike(c))


def binary_op(c: ci.Cursor) -> str:
    return _lib.clang_getBinaryOperatorKindSpelling(_lib.clang_getCursorBinaryOperatorKind(c))


def clang_version() -> str:
    return _lib.clang_getClangVersion()


def rel(root: str, name: str | None) -> str | None:
    if name is None:
        return None
    p = os.path.normpath(os.path.join(root, name))
    r = os.path.relpath(p, root)
    return None if r.startswith("..") else r
