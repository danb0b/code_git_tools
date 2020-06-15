# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 13:36:47 2018

@author: danaukes
"""

import yaml
from git import Repo
import git
import pydevtools.git_stuff.git_tools as git_tools
    
if __name__=='__main__':


    with open('gits_local.yaml') as f:
        local = yaml.load(f)
    
    with open('gits_github.yaml') as f:
        github = yaml.load(f)    
        
    for item in local:
        item
    
    nonlocal_github_urls=git_tools.diff(local,github)
    
    #p1 = os.path.expanduser('~')
    with open('gits_diff.yaml','w') as f:
        github = yaml.dump(nonlocal_github_urls,f)    
        
    print(nonlocal_github_urls)