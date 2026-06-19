#!/usr/bin/env python3
import subprocess, sys
proc = subprocess.run([sys.executable, '/Users/wangweiyang/GitHub/weiyangzen/learn_humanize/tools/branch_research.py', 'verify', 'feature/codex-bypass-sandbox-env'], text=True)
sys.exit(proc.returncode)
