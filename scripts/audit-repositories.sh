#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if command -v python3 >/dev/null 2>&1; then
    python_cmd=python3
elif command -v python >/dev/null 2>&1; then
    python_cmd=python
else
    echo "error: Python 3 is required" >&2
    exit 2
fi

exec "$python_cmd" "$script_dir/audit_repositories.py" "$@"
