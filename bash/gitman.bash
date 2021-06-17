#!/bin/bash
MY_PATH="`dirname \"$0\"`"

python3 $MY_PATH/../python/git_manage/gitman.py --config="$MY_PATH/../support/config.yaml" "$@"
