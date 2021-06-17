@echo off
python %~dp0..\python\git_manage\scripts\gt_reset_to_remote.py --exclude_local="%~dp0..\support\exclude_local.yaml"
