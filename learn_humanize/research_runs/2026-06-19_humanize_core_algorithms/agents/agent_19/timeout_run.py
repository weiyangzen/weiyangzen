#!/usr/bin/env python3
import subprocess
import sys

timeout_seconds = int(sys.argv[1])
stdin_path, stdout_path, stderr_path = sys.argv[2:5]
cmd = sys.argv[5:]
with open(stdin_path, 'rb') as stdin_f, open(stdout_path, 'wb') as stdout_f, open(stderr_path, 'wb') as stderr_f:
    try:
        proc = subprocess.run(cmd, stdin=stdin_f, stdout=stdout_f, stderr=stderr_f, timeout=timeout_seconds)
        raise SystemExit(proc.returncode)
    except subprocess.TimeoutExpired:
        stderr_f.write(f'portable timeout expired after {timeout_seconds}s\n'.encode())
        raise SystemExit(124)
