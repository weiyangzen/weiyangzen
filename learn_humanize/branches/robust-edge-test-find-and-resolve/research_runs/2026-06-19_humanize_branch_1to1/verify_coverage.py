#!/usr/bin/env python3
import subprocess, sys
proc = subprocess.run([sys.executable, '/Users/wangweiyang/GitHub/weiyangzen/learn_humanize/tools/branch_research.py', 'verify', 'robust-edge-test-find-and-resolve'], text=True)
sys.exit(proc.returncode)
