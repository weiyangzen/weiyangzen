#!/usr/bin/env python3
import subprocess, sys
proc = subprocess.run([sys.executable, '/Users/wangweiyang/GitHub/weiyangzen/learn_humanize/tools/branch_research.py', 'verify', 'add-careful-mode-v1.6.5'], text=True)
sys.exit(proc.returncode)
