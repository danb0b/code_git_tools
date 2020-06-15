# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 10:48:56 2018

@author: danaukes
"""

import pydevtools.git_stuff.git_tools as git_tools
import yaml

if __name__=='__main__':
    filename=- 'gits_diff.yaml'
    with open(filename) as f:
        repo_addresses = yaml.load(f)
    git_tools.clone_list(repo_addresses)