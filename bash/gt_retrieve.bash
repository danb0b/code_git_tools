#!/bin/bash

MY_PATH="`dirname \"$0\"`"

python3 $MY_PATH/../python/git_manage/scripts/gt_retrieve.py --exclude_local="$MY_PATH/exclude_local_retrieve.yaml" --exclude_remote="$MY_PATH/exclude_remote.yaml"

