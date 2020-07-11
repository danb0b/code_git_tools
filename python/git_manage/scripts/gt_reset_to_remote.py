# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 20:18:03 2019

@author: danaukes
"""
import os

import os
from git import Repo
import git
import getpass

import requests

import git_manage.git_tools as git_tools
import argparse
import yaml


if __name__=='__main__':
   
    parser = argparse.ArgumentParser()
    parser.add_argument('--exclude_local',dest='exclude_local_f',default = None)
    args=parser.parse_args()
    
    if args.exclude_local_f:
        with open(args.exclude_local_f) as f:
            exclude = yaml.load(f)
    else:
        exclude = None

    p1 = os.path.abspath(os.path.expanduser('~'))
    search_depth = 5

    git_list = git_tools.find_repos(p1,search_depth = 5,exclude=exclude)

    not_synced = []
    for item in git_list:
        print(item)
        r = Repo(item)
    #    for b in r.branches:
        b = r.active_branch
        rem = b.tracking_branch()
        if b.commit.hexsha != rem.commit.hexsha:
            if not r.is_dirty(untracked_files=True):
                if r.is_ancestor(b.commit,rem.commit):
                    print('Yes')
#                    r.head.reset(rem.commit)
                    r.head.reset(rem.commit,index=True,working_tree=True)
                    for item2 in r.untracked_files:
                        os.remove(os.path.join(item,item2))
                    
