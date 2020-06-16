# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 08:52:22 2018

@author: daukes
"""

import os
from git import Repo
import git
import getpass

from github import Github

def retrieve_nonlocal_repos(search_path=None,search_depth = 5,exclude = None,repo_path = None,exclude_remote = None,user = None):
    repo_path = repo_path or os.path.join(os.path.abspath(os.path.expanduser('~')),'repositories')
    if not (os.path.exists(repo_path) and os.path.isdir(repo_path)):
        os.mkdir(repo_path)
    exclude_remote = exclude_remote or []
    
    gits_local = find_repos(search_path,search_depth,exclude)
    print('local gits: ', gits_local)
    gits_remote,owners = scan_github(user=user)
    print('remote gits: ', gits_remote)
    nonlocal_github_urls=diff(gits_local,gits_remote)
    remaining = list(set(nonlocal_github_urls).difference(set(exclude_remote)))
    print('diff: ', remaining)
    clone_list(remaining,repo_path,owners)    
#
    
#
def get_all_repos(user = None):

    user = user or input('username: ')
    password = getpass.getpass('Password: ')

    g = Github(user, password)

    all_repos =  list(g.get_user().get_repos())
    return all_repos 
    
def scan_github(user = None):
    all_gits = []
    owners = {}
    for repo in get_all_repos(user):
        all_gits.append(repo.clone_url)
        owners[repo.clone_url]=repo.owner.login
    return all_gits,owners

def diff(local,github):    
    local_dict = {}
    local_urls = []
    for ii,item in enumerate(local):
    
        try:
            urls = []
            
            repo = Repo(item)
            for r in repo.remotes:
                urls.extend(r.urls)
            local_dict[item] = urls
            local_urls.extend(urls)
        except:
            pass        
    
    local_urls = set(local_urls)
    github_urls = set(github)
    
    nonlocal_github_urls =  list(github_urls-local_urls)
    return nonlocal_github_urls

def find_repos(search_path=None,search_depth=5,exclude=None):
    search_path = search_path or os.path.abspath(os.path.expanduser('~'))

    fp0 = os.path.normpath(os.path.abspath(search_path))
    base_depth = len(fp0.split(os.path.sep))
    
    exclude = exclude or [] 
    
    path_list = [search_path]
    git_list = []
    
    
    while len(path_list)>0:
        current_path = path_list.pop(0)
        fp = os.path.normpath(os.path.abspath(current_path))
        depth = len(fp.split(os.path.sep))
        
#        print(current_path)
        subpath = os.path.join(current_path,'.git')
        if os.path.isdir(subpath):
            git_list.append(current_path)
        else:
            if depth-base_depth<=search_depth:
                try:
                    subdirs = os.listdir(current_path)
                    subdirs = [os.path.join(current_path,item) for item in subdirs]
                    subdirs = [item for item in subdirs if os.path.isdir(item)]
                    subdirs = [item for item in subdirs if not item in exclude]
                    
                    path_list.extend(subdirs)
                except PermissionError:
                    pass
                except FileNotFoundError:
                    pass
    return git_list

def clone_list(repo_addresses,full_path,owners):
    for url in repo_addresses:
        name=(url.split('/')[-1]).split('.')[0]
    #    name = [item for item in name if item!='']
        owner = owners[url]
        local_dest = os.path.normpath(os.path.join(full_path,owner,name))
        if not (os.path.exists(local_dest) and os.path.isdir(local_dest)):
            os.makedirs(local_dest)
        print('cloning ',url, local_dest)
        repo = Repo.clone_from(url,local_dest)

def check_dirty(git_list):    
    dirty = []
    no_path = []
    git_list2 = []

    ll = len(git_list)
    for ii,item in enumerate(git_list):
        print('{0:.0f}/{1:.0f}'.format(ii,ll),item)
        try:
            repo = Repo(item)
            if repo.is_dirty(untracked_files=True):
                dirty.append(item)
            git_list2.append(item)
        except git.NoSuchPathError as e:        
            no_path.append((item,e))

    return git_list2,dirty,no_path

def fetch(git_list):    

    unmatched = []
    git_command_error = []
    git_list2 = []
    no_path = []

    ll = len(git_list)
    for ii,item in enumerate(git_list):
        print('{0:.0f}/{1:.0f}'.format(ii,ll),item)
        try:
            repo = Repo(item)
            
            fetches = repo.remotes[0].fetch()
            if repo.commit().hexsha != fetches[0].commit.hexsha:
                unmatched.append(item)
            git_list2.append(item)
        except git.NoSuchPathError as e:        
            no_path.append((item,e))
        except git.GitCommandError as e:        
            git_command_error.append((item,e))
    
    return git_list2,unmatched,no_path,git_command_error
    
def check_unmatched(git_list):    

    unmatched = []
    git_command_error = []
    git_list2 = []
    no_path = []

    ll = len(git_list)
    for ii,item in enumerate(git_list):
        print('{0:.0f}/{1:.0f}'.format(ii,ll),item)
        try:
#            print(item)
            r = Repo(item)
            b = r.active_branch
            if b.commit.hexsha != b.tracking_branch().commit.hexsha:
                unmatched.append(item)            
            git_list2.append(item)
            
        except git.NoSuchPathError as e:        
            no_path.append((item,e))
        except git.GitCommandError as e:        
            git_command_error.append((item,e))
    
    return git_list2,unmatched,no_path,git_command_error   

if __name__=='__main__':
    r = get_all_repos()
    