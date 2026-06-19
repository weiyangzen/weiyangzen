#!/usr/bin/env python3
import subprocess, sys
proc = subprocess.run([sys.executable, '/Users/wangweiyang/GitHub/weiyangzen/learn_humanize/tools/branch_research.py', 'verify', 'add-a-final-code-simplifier-after-codex-complete'], text=True)
sys.exit(proc.returncode)
