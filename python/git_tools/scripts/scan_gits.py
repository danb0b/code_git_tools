# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 19:40:00 2018

@author: danaukes
"""

#import sys
import os
import yaml
import pydevtools.git_stuff.git_tools as git_tools

if __name__=='__main__':
    
    p1 = os.path.expanduser('~')
    path_list = [p1]
    search_depth = 5
    
    exclude = []
    exclude.append('C:\\Users\\danaukes\\Dropbox (ASU)\\code_external')
    exclude.append('C:\\Users\\daukes\\Dropbox (ASU)\\code_external')
    
    git_list = git_tools.find_repos(path_list,search_depth,exclude)
    
    with open('gits_local.yaml','w') as f:
        yaml.dump(git_list,f)
    
