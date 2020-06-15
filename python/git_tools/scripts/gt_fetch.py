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
    exclude.append(os.path.join(os.path.abspath(os.path.expanduser('~')),'repositories\dormant'))
    exclude.append(os.path.join(os.path.abspath(os.path.expanduser('~')),'Arizona State University'))
    git_list = git_tools.find_repos(p1,search_depth = 5,exclude=exclude)

    git_list3,unmatched,no_path2,git_command_error = git_tools.fetch(git_list)
    print('---------')
    print('Unmatched:')
    for item in unmatched:
        print(item)
    print('---------')
    print('No Path:')
    for item,e in no_path2:
        print(item,e)
    print('---------')
    print('Git Command:')
    for item,e in git_command_error:
        print(item,e)
    print('---------')