#!/usr/bin/env bash
#
# Run the full test suite once per installed HTML parser backend, so we know
# the tests hold no matter what parseString() was pointed at.
#
#   scripts/test_all_backends.sh                     # every known backend
#   scripts/test_all_backends.sh html5lib lxml_html  # just these
#
# A backend that is not installed is reported as skipped, not failed.
# Tests that pass parser= explicitly are unaffected; this only moves the
# default used when parseString() is called with no parser.

set -u

PYTHON="${PYTHON:-./venv/bin/python}"
BACKENDS=("$@")
if [ ${#BACKENDS[@]} -eq 0 ]; then
    BACKENDS=(turbohtml html.parser html5lib lxml_html selectolax markupever justhtml reliq tl)
fi

rc=0
declare -a summary
for backend in "${BACKENDS[@]}"; do
    echo
    echo "=================================================================="
    echo " backend: ${backend}"
    echo "=================================================================="
    out=$("$PYTHON" -m pytest tests/ -q -p no:randomly \
        --parser-backend="${backend}" 2>&1)
    echo "$out" | tail -n 20
    line=$(echo "$out" | grep -E "passed|error|no tests ran" | tail -n 1)
    if echo "$out" | grep -q "is not usable here\|Unknown parser"; then
        summary+=("${backend}: SKIPPED (not installed)")
    elif echo "$out" | grep -qE "failed|error"; then
        summary+=("${backend}: ${line}")
        rc=1
    else
        summary+=("${backend}: ${line}")
    fi
done

echo
echo "=================================================================="
echo " summary"
echo "=================================================================="
for row in "${summary[@]}"; do
    echo "  ${row}"
done
exit "$rc"
