#!/usr/bin/env bash
# Judge Pintos tests that the week's `make dfast` runs.
#
#   run-tests.sh [--wait-loop] <tree> <jobs> <timeout> [<dir/test>...]
#   run-tests.sh --selftest <tree>
#   e.g. run-tests.sh --wait-loop /tmp/wt/nuri 7 5 threads/alarm-single userprog/args-none
#
# <tree> holds pintos/ and the week GNUmakefile. That file owns docker, icount
# SHIFT, JOBS and TIMEOUT; its `dfast` label takes TESTS= (short test names).
# No test list: run every test the build knows (the full run on the control).
#
# One line per test: <verdict> <dir/test>
#   PASS      the upstream .ck passed.
#   PASS*     passed after the shutdown lines were appended to a TIMEOUT run.
#             Only with --wait-loop, only for userprog/ and filesys/ tests.
#             A hang after the last output line is not detected.
#   FAIL      the upstream .ck failed. Any other TIMEOUT is FAIL (threads
#             tests run without process_wait, so a TIMEOUT there is a hang).
#   UNJUDGED  a PASS* candidate whose .ck has no check_expected (halt, the
#             filesys persistence tests): the shutdown itself is its verdict,
#             so a rewrite cannot judge it.
#   STALE     the .output is older than this run (build failed or not run).
#
# --wait-loop: pass it only for a tree whose process_wait loop is cited by file:line.
# --selftest:  judge the fixtures next to this script with <tree>'s real .ck files.
set -euo pipefail
here=$(dirname "$(realpath "$0")")
die() { echo "run-tests.sh: $*" >&2; exit 2; }

# judge <tree> <output file> <dir/test> <wait-loop 0|1>
judge() {
  local tree=$1 o=$2 spec=$3 wl=$4 t=tests/$3 ck=$1/pintos/tests/$3.ck d cmd v
  [ -f "$ck" ] || die "no $ck"
  if [ "$(tail -n1 "$o")" = TIMEOUT ]; then
    case "$wl:$spec" in 1:userprog/*|1:filesys/*) ;; *) echo "FAIL $spec"; return ;; esac
    if ! grep -q check_expected "$ck"; then echo "UNJUDGED $spec"; return; fi
    d=$(mktemp -d); mkdir -p "$d/$(dirname "$t")"
    cmd=$(grep -o "Executing '[^']*'" "$o" | sed 's/Executing //' || true)
    { grep -v '^TIMEOUT' "$o"; echo "Execution of $cmd complete."
      printf 'Timer: 0 ticks\nPowering off...\n'; } > "$d/$t.output"
    v=$(cd "$d" && perl -I"$tree/pintos" "$ck" "$t" "$t.result" >/dev/null 2>&1; head -1 "$t.result")
    [ "$v" = PASS ] && v='PASS*'
  else
    d=$(mktemp -d); mkdir -p "$d/$(dirname "$t")"; cp "$o" "$d/$t.output"
    v=$(cd "$d" && perl -I"$tree/pintos" "$ck" "$t" "$t.result" >/dev/null 2>&1; head -1 "$t.result")
  fi
  rm -rf "$d"
  echo "$v $spec"
}

if [ "${1:-}" = --selftest ]; then
  tree=$(realpath "${2:?usage: run-tests.sh --selftest <tree>}"); f=$here/fixtures; bad=0
  while read -r want wl spec file; do
    got=$(judge "$tree" "$f/$file" "$spec" "$wl" | cut -d' ' -f1)
    if [ "$got" = "$want" ]; then echo "ok       $want $spec (wait-loop=$wl)"
    else echo "MISMATCH want $want got $got $spec (wait-loop=$wl)"; bad=1; fi
  done <<'EOF'
FAIL     1 threads/alarm-single  threads/alarm-single.timeout.output
UNJUDGED 1 userprog/halt         userprog/halt.timeout.output
FAIL     0 userprog/args-single  userprog/args-single.timeout.output
PASS*    1 userprog/args-single  userprog/args-single.timeout.output
PASS     1 threads/alarm-single  threads/alarm-single.complete.output
EOF
  exit $bad
fi

wl=0; [ "${1:-}" = --wait-loop ] && { wl=1; shift; }
[ $# -ge 3 ] || die "usage: run-tests.sh [--wait-loop] <tree> <jobs> <timeout> [<dir/test>...]"
tree=$(realpath "$1"); jobs=$2; timeout=$3; shift 3
[ -f "$tree/GNUmakefile" ] || die "no $tree/GNUmakefile"
build=$(make -s -p -q -C "$tree" 2>/dev/null | sed -n 's/^BUILD := //p' | head -1 || true)
[ -n "$build" ] || die "no BUILD in $tree/GNUmakefile"
make -s -n -C "$tree" dfast >/dev/null 2>&1 || die "no dfast label in $tree/GNUmakefile"
for spec in "$@"; do [ -f "$tree/pintos/tests/$spec.ck" ] || die "no .ck for $spec"; done

log=$(mktemp); marker=$(mktemp)
names=$(printf '%s\n' "$@" | sed 's#.*/##' | tr '\n' ' ')
make -C "$tree" dfast DOCKER_TTY=-i JOBS="$jobs" TIMEOUT="$timeout" ${names:+TESTS="$names"} \
  >"$log" 2>&1 || true

if [ $# -eq 0 ]; then
  set -- $(make -s --no-print-directory -C "$tree/$build" \
             --eval 'print-tests: ; @echo $(TESTS)' print-tests 2>/dev/null | sed 's#tests/##g')
  [ $# -gt 0 ] || die "build failed, no test list: $log"
fi
for spec in "$@"; do
  o=$tree/$build/tests/$spec.output
  if [ ! "$o" -nt "$marker" ]; then echo "STALE $spec ($log)"; continue; fi
  judge "$tree" "$o" "$spec" "$wl"
done
