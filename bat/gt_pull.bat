@echo off
python %~dp0..\python\git_manage\scripts\gt_fetch.py --exclude_local="%~dp0..\support\exclude_local.yaml"
