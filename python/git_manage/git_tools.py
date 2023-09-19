# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 08:52:22 2018

@author: daukes
"""

import os
from git import Repo
import git
from github import Github
import yaml

def retrieve_nonlocal_repos(git_list,repo_path,user,token,exclude_remote = None,verbose=True):
    if not (os.path.exists(repo_path) and os.path.isdir(repo_path)):
        os.mkdir(repo_path)

    if verbose:
        print('local gits: ', git_list)
    nonlocal_github_urls,owners,owner_repo_dict = list_nonlocal_repos(git_list,user,token,verbose)
    remaining =list(set(nonlocal_github_urls) - set(format_repo_list(exclude_remote,destination_format='ssh',user=user)))
    if verbose:
        print('diff: ', remaining)
    
    clone_list(remaining,repo_path,owners,user)    

def list_nonlocal_repos(git_list,user,token,verbose=False):
    gits_remote_formatted,owners,owner_repo_dict = list_remote_repos(user, token,verbose,format_local=True)
    nonlocal_github_urls=diff(git_list,gits_remote_formatted)
    return nonlocal_github_urls,owners,owner_repo_dict

def list_remote_repos(user,token,verbose=False,format_local=False):
    gits_remote,owners,owner_repo_dict = scan_github(token)
    if verbose:
        print('remote gits: ', gits_remote)
    if format_local:
        gits_remote = [local_ssh_from_url_user(item, user) for item in gits_remote]
    return gits_remote,owners,owner_repo_dict

def get_all_repos(token):
    g = Github(token)

    all_repos =  list(g.get_user().get_repos())
    return all_repos 
    
def scan_github(token):
    all_gits = []
    owners = {}
    owner_repo_dict = {}
    for repo in get_all_repos(token):
        all_gits.append(repo.clone_url)
        owners[repo.clone_url]=repo.owner.login
        try:
            owner_repo_dict[repo.owner.login].append(repo.clone_url)
        except KeyError:
            owner_repo_dict[repo.owner.login] = []
            owner_repo_dict[repo.owner.login].append(repo.clone_url)
    return all_gits,owners,owner_repo_dict

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

def is_ssh_format(item):
    return item.startswith('git@')

def is_github_clone_format(item):
    return item.startswith('https://github.com/')

def format_repo_list(list_in,destination_format='github',user=None):
    list_out = []
    for item in list_in:
        if is_ssh_format(item):
            if destination_format=='github':
                list_out.append(remote_url_from_ssh_address(item))
            elif destination_format=='ssh':
                list_out.append(item)
            else:
                raise(Exception('format not specified'))
        elif is_github_clone_format(item):
            if destination_format=='github':
                list_out.append(item)
            elif destination_format=='ssh':
                list_out.append(local_ssh_from_url_user(item, user))                
            else:
                raise(Exception('format not specified'))
        else:
            raise(Exception('format not identified'))
    return list_out
            

def local_ssh_from_url_user(url,user):
        a,b = url.split('github.com/')
        # b1,b2 = b.split('/')
        # owner = b1
        # reponame = b2
        # reponame = (url.split('/')[-1])
        # repoowner = (url.split('/')[-2])
        newurl = 'git@'+user+'.github.com:'+b
        return newurl
    
def remote_urls_from_folder(local_folder):
    r = Repo(local_folder)
    remote = r.remote()
    ssh = remote.url
    return remote_url_from_ssh_address(ssh)

def remote_url_from_ssh_address(local_ssh_address):
    a = 'https://github.com/'
    b = local_ssh_address.split(':')[-1]
    c = ''.join([a,b])
    return c

def clone_list(repo_addresses,full_path,owners,user):
    owners2 = dict([(local_ssh_from_url_user(url, user),owners[url]) for url in owners.keys()])
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
            
        
        print('cloning url:',url,'to: ',local_dest)

        repo = Repo.clone_from(url,local_dest)

def check_dirty(git_list,verbose=False):    
    
    dict1 = {}
    dict1['dirty'] = []
    dict1['no_path'] = []
    dict1['git_list']= []

    ll = len(git_list)
    for ii,item in enumerate(git_list):
        if verbose:
            print('{0:.0f}/{1:.0f}'.format(ii+1,ll),item)
        try:
            repo = Repo(item)
            if repo.is_dirty(untracked_files=True):
                dict1['dirty'].append(item)
            dict1['git_list'].append(item)
        except git.NoSuchPathError as e:        
            dict1['no_path'].append((item,e))

    # if verbose:
        # print('---------')


    # return git_list2,dirty,no_path
    
    return dict1

def get_current_branch(git_list):    
    current_branch={}

    ll = len(git_list)
    for ii,item in enumerate(git_list):
        print('{0:.0f}/{1:.0f}'.format(ii+1,ll),item)
        repo = Repo(item)
        current_branch[item]=str(repo.active_branch)

    return current_branch

def fetch(git_list,verbose = False):    

    git_command_errors = {}
    git_list2 = []

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
            try:   
                git_command_errors[str(e)].append(item)
            except KeyError:
                git_command_errors[str(e)]=[]
                git_command_errors[str(e)].append(item)
        except git.GitCommandError as e:        
            try:   
                git_command_errors[str(e)].append(item)
            except KeyError:
                git_command_errors[str(e)]=[]
                git_command_errors[str(e)].append(item)
            
    if len(git_command_errors)>0:

        print("------------------")
        print("Errors:")
        print(yaml.dump(git_command_errors))
        print("------------------")
    
    
    return git_list2
    
def check_unmatched(git_list,verbose=False):    
    
    dict1 = {}
    dict1['git_command_error'] = {}
    dict1['no_path'] = []
    dict1['missing_local_branches'] = {}
    dict1['missing_remote_branches'] = {}
    dict1['unsynced_branches'] = {}

    ll = len(git_list)
    for ii,repo_path in enumerate(git_list):
        if verbose:
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
                    try:
                        if branch.commit.hexsha != branch.tracking_branch().commit.hexsha:
                            try:
                                dict1['unsynced_branches'][repo_path].append(branch.name)
                            except KeyError:
                                dict1['unsynced_branches'][repo_path]=[]
                                dict1['unsynced_branches'][repo_path].append(branch.name)
                    except ValueError:
                        try:
                            dict1['missing_remote_branches'][repo_path].append(branch.name)
                        except KeyError:
                            dict1['missing_remote_branches'][repo_path]=[]
                            dict1['missing_remote_branches'][repo_path].append(branch.name)

                else:
                    try:
                        dict1['missing_remote_branches'][repo_path].append(branch.name)
                    except KeyError:
                        dict1['missing_remote_branches'][repo_path]=[]
                        dict1['missing_remote_branches'][repo_path].append(branch.name)
                
            b_s = [branch.tracking_branch() for branch in r.branches]
            b_s = [branch for branch in b_s if branch is not None]
            b_s = set(b_s)
            not_local = list(remote_branches_s.difference(b_s))
            for ref in not_local:
                try:
                    dict1['missing_local_branches'][repo_path].append(ref.name)
                except KeyError:
                    dict1['missing_local_branches'][repo_path]=[]
                    dict1['missing_local_branches'][repo_path].append(ref.name)
                        
            
        except git.NoSuchPathError as e:        
            dict1['no_path'].append(repo_path)
                
        except git.GitCommandError as e:        
            dict1['git_command_error'].append(repo_path)
                
    
    # print('---------')
    # print('Missing Local Branches:')
    # for item in dict1['missing_local_branches']:
    #     print(item)
    # print('---------')
    # print('Missing Remote Branches:')
    # for item in dict1['missing_remote_branches']:
    #     print(item)
    # print('---------')
    # print('Branches Unsynced:')
    # for item in dict1['unsynced_branches']:
    #     print(item)
    # print('---------')
    # print('No Path:')
    # for item,e in dict1['no_path']:
    #     print(item,e)
    # print('---------')
    # print('Git Command:')
    # for item,e in dict1['git_command_error']:
    #     print(item,e)
    # print('---------')

    # return git_list2,unmatched,no_path,git_command_error   

    return dict1

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
    # r = get_all_repos()
    pass
    
