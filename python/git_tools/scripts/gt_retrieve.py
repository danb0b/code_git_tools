# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 16:06:40 2019

@author: daukes
"""
import os
import yaml
import git_tools.git_tools as git_tools

if __name__=='__main__':
    exclude = []
    exclude.append(os.path.join(os.path.abspath(os.path.expanduser('~')),'Dropbox (ASU)\\code_external'))
    exclude.append(os.path.join(os.path.abspath(os.path.expanduser('~')),'Arizona State University'))
    search_path = os.path.abspath(os.path.expanduser('~'))

    exclude_remote = []
    exclude_remote.append('https://github.com/msharifzadeh/Comprehensive_Presentation.git')
    exclude_remote.append('https://github.com/msharifzadeh/Comprehensive_Exam_Mohammad_Sharifzadeh.git')
    exclude_remote.append('https://github.com/cdbrauer/VoxelFuse.git')
    exclude_remote.append('https://github.com/cdbrauer/Material-Interface-Generation.git')
    exclude_remote.append('https://github.com/ThomasSugar/hmil.git')
    git_tools.retrieve_nonlocal_repos(search_path,exclude = exclude, exclude_remote=exclude_remote,user = 'danaukes')
    git_tools.retrieve_nonlocal_repos(search_path,exclude = exclude, exclude_remote=exclude_remote,user = 'danb0b')    