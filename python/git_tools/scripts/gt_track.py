# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 20:18:03 2019

@author: danaukes
"""
import os

import git_tools.git_tools as git_tools


if __name__=='__main__':
   
    p1 = os.path.abspath(os.path.expanduser('~'))
    search_depth = 5
    exclude=[]
    exclude.append(os.path.join(os.path.abspath(os.path.expanduser('~')),'Dropbox (ASU)\\code_external'))
    exclude.append(os.path.join(os.path.abspath(os.path.expanduser('~')),'repositories\\dormant'))
    exclude.append(os.path.join(os.path.abspath(os.path.expanduser('~')),'Arizona State University'))
    git_list = git_tools.find_repos(p1,search_depth = 5,exclude=exclude)

    git_list2,dirty,no_path = git_tools.check_dirty(git_list)
    print('---------')
    print('Dirty:')
    for item in dirty:
        print(item)
    print('---------')
    print('No Path:')
    for item,e in no_path:
        print(item,e)
