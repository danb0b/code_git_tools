# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 08:52:22 2018

@author: daukes
"""

import os
from git import Repo
import git

from github import Github

def retrieve_nonlocal_repos(git_list,repo_path,user,token,exclude_remote = None,verbose=True):
    if not (os.path.exists(repo_path) and os.path.isdir(repo_path)):
        os.mkdir(repo_path)

    if verbose:
        print('local gits: ', git_list)
    nonlocal_github_urls,owners = list_nonlocal_repos(git_list,user,token,verbose)
    for blacklist_item in exclude_remote:
        nonlocal_github_urls=[item for item in nonlocal_github_urls if blacklist_item not in item]
    exclude_remote = exclude_remote or []
    remaining = list(set(nonlocal_github_urls).difference(set(exclude_remote)))
    if verbose:
        print('diff: ', remaining)
    
    clone_list(remaining,repo_path,owners,user)    

def list_nonlocal_repos(git_list,user,token,verbose=False):
    gits_remote_formatted,owners = list_remote_repos(user, token,verbose)
    nonlocal_github_urls=diff(git_list,gits_remote_formatted)
    return nonlocal_github_urls,owners

def list_remote_repos(user,token,verbose=False):
    gits_remote,owners = scan_github(token)
    if verbose:
        print('remote gits: ', gits_remote)
    gits_remote_formatted = [reform_repo_name(item, user) for item in gits_remote]
    return gits_remote_formatted,owners

def get_all_repos(token):


    g = Github(token)

    all_repos =  list(g.get_user().get_repos())
    return all_repos 
    
def scan_github(token):
    all_gits = []
    owners = {}
    for repo in get_all_repos(token):
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

def reform_repo_name(url,user):
        reponame = (url.split('/')[-1])
        repoowner = (url.split('/')[-2])
        newurl = 'git@'+user+'.github.com:'+repoowner+'/'+reponame
        return newurl
    

def clone_list(repo_addresses,full_path,owners,user):
    owners2 = dict([(reform_repo_name(url, user),owners[url]) for url in owners.keys()])
    for url in repo_addresses:
        reponame = (url.split('/')[-1])
        name=reponame.split('.')
        name='.'.join([item for item in name if item!='git'])
        
        owner = owners2[url]
        ii = 1
        local_dest = os.path.normpath(os.path.join(full_path,owner,name))
        
        while (os.path.exists(local_dest) and os.path.isdir(local_dest)):
            name = name+'_'+str(ii)
            local_dest = os.path.normpath(os.path.join(full_path,owner,name))
            ii+=1
        os.makedirs(local_dest)
            
        
        # newurl = reform_repo_name(url, user)
        print('cloning url:',url,'to: ',local_dest)

        repo = Repo.clone_from(url,local_dest)

def check_dirty(git_list):    
    dirty = []
    no_path = []
    git_list2 = []

    ll = len(git_list)
    for ii,item in enumerate(git_list):
        print('{0:.0f}/{1:.0f}'.format(ii+1,ll),item)
        try:
            repo = Repo(item)
            if repo.is_dirty(untracked_files=True):
                dirty.append(item)
            git_list2.append(item)
        except git.NoSuchPathError as e:        
            no_path.append((item,e))

    return git_list2,dirty,no_path

def fetch(git_list,verbose = True):    

    unmatched = []
    git_command_error = []
    git_list2 = []
    no_path = []

    ll = len(git_list)
    for ii,item in enumerate(git_list):
        print('{0:.0f}/{1:.0f}'.format(ii+1,ll),item)
        try:
            repo = Repo(item)
            
            fetches = repo.remotes[0].fetch()
            # if repo.commit().hexsha != fetches[0].commit.hexsha:
                # unmatched.append(item)
            git_list2.append(item)
        except git.NoSuchPathError as e:        
            no_path.append((item,e))
        except git.GitCommandError as e:        
            git_command_error.append((item,e))
            
    if verbose:
    
        print('---------')
        print('No Path:')
        for item,e in no_path:
            print(item,e)
        print('---------')
        print('Git Command:')
        for item,e in git_command_error:
            print(item,e)
        print('---------')
    
    return git_list2
    
def check_unmatched(git_list,verbose=True):    

    git_command_error = []
    no_path = []
    missing_local_branches = []
    missing_remote_branches = []
    unsynced_branches = []
    
    ll = len(git_list)
    for ii,repo_path in enumerate(git_list):
        print('{0:.0f}/{1:.0f}'.format(ii+1,ll),repo_path)
        try:
            r = Repo(repo_path)
            
            remote_branches = []
            for rr in r.remote().refs:
                if not rr.name.lower().endswith('/head'):
                    remote_branches.append(rr)
            remote_branches_s = set(remote_branches)
            
            
            for branch in r.branches:
                if branch.tracking_branch() is not None:
                    if branch.commit.hexsha != branch.tracking_branch().commit.hexsha:
                        unsynced_branches.append((repo_path,branch.name))
                else:
                    missing_remote_branches.append((repo_path,branch.name))
                
            b_s = [branch.tracking_branch() for branch in r.branches]
            b_s = [branch for branch in b_s if branch is not None]
            b_s = set(b_s)
            not_local = list(remote_branches_s.difference(b_s))
            for ref in not_local:
                missing_local_branches.append((repo_path,ref.name))
            
        except git.NoSuchPathError as e:        
            no_path.append((repo_path,e))
        except git.GitCommandError as e:        
            git_command_error.append((repo_path,e))
    
    if verbose:
    
        print('---------')
        print('Missing Local Branches:')
        for item in missing_local_branches:
            print(item)
        print('---------')
        print('Missing Remote Branches:')
        for item in missing_remote_branches:
            print(item)
        print('---------')
        print('Branches Unsynced:')
        for item in unsynced_branches:
            print(item)
        print('---------')
        print('No Path:')
        for item,e in no_path:
            print(item,e)
        print('---------')
        print('Git Command:')
        for item,e in git_command_error:
            print(item,e)
        print('---------')
    
    # return git_list2,unmatched,no_path,git_command_error   

def reset_branches(git_list,verbose=True):    

    git_command_error = []
    no_path = []
    
    ll = len(git_list)
    for ii,repo_path in enumerate(git_list):
        print('{0:.0f}/{1:.0f}'.format(ii+1,ll),repo_path)
        try:
            r = Repo(repo_path)
            
            # remote_branches = []
            # for rr in r.remote().refs:
                # if not rr.name.lower().endswith('/head'):
                    # remote_branches.append(rr)
            # remote_branches_s = set(remote_branches)
            
            active_branch = r.active_branch
            
            try:
                
                if not r.is_dirty(untracked_files=True):
                    
                    for branch in r.branches:
                        if branch.tracking_branch() is not None:
    
                            tb = branch.tracking_branch()
                            if r.is_ancestor(branch.commit,tb.commit):
                                if branch.commit.hexsha != tb.commit.hexsha:
                                    branch.checkout()
                                    r.head.reset(tb.commit,index=True,working_tree=True)
                                    print('Yes')
            except Exception as e:
                print(e)
            finally:
                active_branch.checkout()
        except git.NoSuchPathError as e:        
         no_path.append((repo_path,e))
        except git.GitCommandError as e:        
            git_command_error.append((repo_path,e))   

if __name__=='__main__':
    r = get_all_repos()
    
