#!/usr/bin/sh
python setup.py bdist_wheel
docker build -t gitman ./