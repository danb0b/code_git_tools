#!/usr/bin/sh

echo "export PATH=\$PATH:$PWD/bash" >> ~/.bashrc
echo "export PATH=\$PATH:$PWD/python/git_manage" >> ~/.bashrc
chmod +x python/git_manage/gitman.py
chmod +x *.sh
chmod +x *.bash
