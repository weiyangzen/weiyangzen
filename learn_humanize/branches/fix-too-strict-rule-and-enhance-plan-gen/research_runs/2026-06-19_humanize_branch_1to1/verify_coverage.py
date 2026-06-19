#!/usr/bin/env python3
import subprocess, sys
proc = subprocess.run([sys.executable, '/Users/wangweiyang/GitHub/weiyangzen/learn_humanize/tools/branch_research.py', 'verify', 'fix-too-strict-rule-and-enhance-plan-gen'], text=True)
sys.exit(proc.returncode)
