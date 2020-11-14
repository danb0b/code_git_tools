@echo off

python %~dp0..\python\git_manage\scripts\gt_retrieve.py --exclude_local="%~dp0exclude_local_retrieve.yaml" --exclude_remote="%~dp0exclude_remote.yaml"
