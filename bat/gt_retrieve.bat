@echo off

python %~dp0..\python\git_manage\scripts\gt_retrieve.py --exclude_local="%~dp0..\support\exclude_local_retrieve.yaml" --exclude_remote="%~dp0..\support\exclude_remote.yaml"
