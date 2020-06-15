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
from lxml import etree
from lxml import html

import pydevtools.git_stuff.git_tools as git_tools


if __name__=='__main__':
   
    p1 = os.path.abspath(os.path.expanduser('~'))
    search_depth = 5
    exclude=[]
    exclude.append(os.path.join(os.path.abspath(os.path.expanduser('~')),'Dropbox (ASU)\\code_external'))
    exclude.append(os.path.join(os.path.abspath(os.path.expanduser('~')),'repositories\dormant'))
    exclude.append(os.path.join(os.path.abspath(os.path.expanduser('~')),'Arizona State University'))
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
                    
#            base = r.merge_base(b,rem)
#            r.index.merge_tree(b,base=base)
#            r.index.commit('auto_merge', parent_commits=(b.commit, rem.commit))
#            b.checkout(force=False)