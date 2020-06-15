# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 20:18:03 2019

@author: danaukes
"""
import os
import git
from git import Repo

import pydevtools.git_stuff.git_tools as git_tools


if __name__=='__main__':
   
    p1 = os.path.abspath(os.path.expanduser('~'))
    search_depth = 5
    exclude=[os.path.join(os.path.abspath(os.path.expanduser('~')),'Dropbox (ASU)\\code_external')]
    exclude.append(os.path.join(os.path.abspath(os.path.expanduser('~')),'Arizona State University'))
    git_list = git_tools.find_repos(p1,search_depth = 5,exclude=exclude)

#    dirty = []
    no_path = []
    git_list2 = []
    urls = []
#    ll = len(git_list)
    for ii,item in enumerate(git_list):
#        print('{0:.0f}/{1:.0f}'.format(ii,ll),item)
        try:
            repo = Repo(item)
            remote = repo.remote()
            url = list(remote.urls)[0]
            
#            if repo.is_dirty(untracked_files=True):
#                dirty.append(item)
            git_list2.append(item)
            urls.append(url)
        except git.NoSuchPathError as e:        
            no_path.append((item,e))

#    return git_list2,dirty,no_path

    url_dest = {}
    for item in urls:
        url_dest[item]=[]
    for key,value in zip(urls,git_list2):
        url_dest[key].append(value)
    for key,value in url_dest.items():
        if len(value)>1:
            print(key,value)