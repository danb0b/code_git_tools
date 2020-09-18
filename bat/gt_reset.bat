@echo off
python %~dp0..\python\git_manage\scripts\gt_reset_to_remote.py --exclude_local="%~dp0exclude_local.yaml"
