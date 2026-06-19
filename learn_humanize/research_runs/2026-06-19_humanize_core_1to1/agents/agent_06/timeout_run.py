#!/usr/bin/env python3
import subprocess, sys, time, os, signal
if len(sys.argv) < 3:
    print("usage: timeout_run.py SECONDS COMMAND...", file=sys.stderr)
    sys.exit(2)
timeout = int(sys.argv[1])
cmd = sys.argv[2:]
proc = subprocess.Popen(cmd, preexec_fn=os.setsid)
try:
    sys.exit(proc.wait(timeout=timeout))
except subprocess.TimeoutExpired:
    os.killpg(proc.pid, signal.SIGTERM)
    try:
        proc.wait(timeout=20)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.wait()
    sys.exit(124)
