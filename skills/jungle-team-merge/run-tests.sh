#!/usr/bin/env bash
# Run Pintos tests in one tree, in parallel, and judge them.
#
#   run-tests.sh <tree> <jobs> <timeout> <dir/test>...
#   e.g. run-tests.sh /tmp/wt/nuri 7 5 threads/alarm-single userprog/args-none
#
# <tree> holds pintos/ and the week's GNUmakefile (r_<test> labels).
# Prints one line per test: PASS|FAIL|STALE <dir/test> [timeout-judged].
#
# timeout-judged: the run hit TIMEOUT (process_wait still loops), so the
# shutdown lines were appended before the real .ck judged it. That is
# meaningful only for tests whose .ck checks the user program's output; it
# is meaningless for a test that judges the shutdown itself (halt).
# STALE: the .output is older than this run, so it was not judged.
set -euo pipefail
tree=$(realpath "$1"); jobs=$2; timeout=$3; shift 3
build=$tree/pintos/userprog/build
judge=$(mktemp -d)
marker=$judge/.start
touch "$marker"

printf '%s\n' "$@" | sed 's#.*/##' |
  docker run --rm -i --user "$(id -u):$(id -g)" -e HOME=/tmp \
    -e PINTOS_QEMU_EXTRA="-icount shift=5,sleep=off" \
    -v "$tree":/work -w /work pintosdev \
    sh -c "make -s kernel >/dev/null 2>&1 || echo BUILD_FAIL >&2
           xargs -P $jobs -I{} make -s r_{} TIMEOUT=$timeout >/dev/null 2>&1; true"

for spec in "$@"; do
  t=tests/$spec
  o=$build/$t.output
  if [ ! "$o" -nt "$marker" ]; then echo "STALE $spec"; continue; fi
  mkdir -p "$judge/$(dirname "$t")"
  tag=""
  if grep -q TIMEOUT "$o"; then
    cmd=$(grep -o "Executing '[^']*'" "$o" | sed 's/Executing //' || true)
    { grep -v TIMEOUT "$o"; echo "Execution of $cmd complete."
      printf 'Timer: 0 ticks\nPowering off...\n'; } > "$judge/$t.output"
    tag=" timeout-judged"
  else
    cp "$o" "$judge/$t.output"
  fi
  (cd "$judge" && perl -I"$tree/pintos" "$tree/pintos/$t.ck" "$t" "$t.result" \
     >/dev/null 2>&1 || true
   echo "$(head -1 "$t.result") $spec$tag")
done
