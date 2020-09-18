@echo off
echo %~dp0
python %~dp0..\python\git_manage\scripts\gt_track.py --exclude_local="%~dp0exclude_local.yaml"
