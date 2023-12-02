#!/home/danaukes/anaconda3/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 20:18:03 2019

@author: danaukes
"""
import os
import git_manage.git_tools as git_tools
import argparse
import yaml
import sys

command_string='''
branch-status,
clone,
exclude,
find-remote-branches,
index,
list, 
list-github,
list-remotes,
list-github-nonlocal,
list-active-branch,
list-upstream,
list-local-branches,
pull,
reset,
status,
'''

def new_user():
    print('No github accounts present in config')
    user = input('username: ')
    token = input('token: ')
    save = input('save user info? (y/n)')
    save = save.lower()=='y'
    return user,token,save


def clean_path(path_in):
    path_out = os.path.normpath(os.path.abspath(os.path.expanduser(path_in)))
    return path_out

if hasattr(sys, 'frozen'):
    module_path = os.path.normpath(os.path.join(os.path.dirname(sys.executable),''))
else:
    module_path = sys.modules['git_manage'].__path__[0]

support_path = clean_path(os.path.join(module_path, 'support'))
personal_config_folder = clean_path('~/.config/gitman')
personal_config_path = clean_path(os.path.join(personal_config_folder,'config.yaml'))
package_config_path = clean_path(os.path.join(support_path,'config.yaml'))

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('command',metavar='command',type=str,help=command_string, default = '')
    parser.add_argument('--config',dest='config_f',default = None)
    parser.add_argument('--token',dest='token',default = None)
    parser.add_argument('-n','--no-index',dest='no_index',action='store_true', default = False)
    parser.add_argument('-v','--verbose',dest='verbose',action='store_true', default = False)
    parser.add_argument('-u','--user',dest='user',default = 'all')
    
    args = parser.parse_args()
    
    module_path = ''
    
    potential_file_locations = [args.config_f,personal_config_path,package_config_path]
    potential_file_locations = [item for item in potential_file_locations if item is not None]

    for ii,item in enumerate(potential_file_locations):
        try:    
            item = clean_path(item)
            with open(item) as f:
                config = yaml.load(f,Loader=yaml.Loader)
            break
        except TypeError as e:
            print(e)
            if ii==len(potential_file_locations)-1:
                raise Exception('config file not found')
        except FileNotFoundError as e:
            print(e)
            if ii==len(potential_file_locations)-1:
                raise Exception('config file not found')
            
    p1 = clean_path(config['index_location'])

    exclude = config['exclude_local']
    exclude = [clean_path(item) for item in exclude]

    exclude_mod = exclude[:]
    exclude_mod.extend([clean_path(item) for item in config['archive_path']])

    index_cache_path = clean_path(config['index_cache'])
        
    # print('Excluded Paths:', str(exclude_mod))


    if args.command == 'pull':

        git_list = git_tools.index_git_list(p1,not args.no_index,index_cache_path,config['index_depth'],exclude_mod)

        git_list = git_tools.fetch(git_list,args.verbose)
        git_tools.check_unmatched(git_list,args.verbose)

    elif args.command == 'status':
        
        git_list = git_tools.index_git_list(p1,not args.no_index,index_cache_path,config['index_depth'],exclude_mod)

        dict1 = git_tools.check_dirty(git_list,args.verbose)
        if args.verbose:
            s = yaml.dump(dict1)
            print(s)
        else:
            del dict1['git_list']
            s = yaml.dump(dict1)
            print(s)
        # print('Dirty:')
        # for item in dirty:
            # print(item)
        # print('---------')
        # print('No Path:')
        # for item,e in no_path:
            # print(item,e)
        
    elif args.command in ['branch-status','bs','branch_status']:

        git_list = git_tools.index_git_list(p1,not args.no_index,index_cache_path,config['index_depth'],exclude_mod)

        dict1 = git_tools.check_unmatched(git_list,args.verbose)
        del dict1['missing_local_branches']
        s = yaml.dump(dict1)
        print(s)

    elif args.command in ['find-remote-branches']:
        git_list = git_tools.index_git_list(p1,not args.no_index,index_cache_path,config['index_depth'],exclude_mod)

        dict1 = git_tools.check_unmatched(git_list,args.verbose)
        s = yaml.dump(dict1['missing_local_branches'])
        print(s)
        
    elif args.command in ['list-remotes']:
        git_list = git_tools.index_git_list(p1,not args.no_index,index_cache_path,config['index_depth'],exclude_mod)

        dict1 = git_tools.list_remotes(git_list,args.verbose)
        s = yaml.dump(dict1)
        print(s)

    elif args.command in ['list-upstream']:
        git_list = git_tools.index_git_list(p1,not args.no_index,index_cache_path,config['index_depth'],exclude_mod)

        dict1 = git_tools.list_upstream(git_list,args.verbose)
        s = yaml.dump(dict1)
        print(s)

    elif args.command in ['list-local-branches']:
        git_list = git_tools.index_git_list(p1,not args.no_index,index_cache_path,config['index_depth'],exclude_mod)

        dict1 = git_tools.list_local_branches(git_list,args.verbose)
        s = yaml.dump(dict1)
        print(s)

    elif args.command == 'clone':
        git_list = git_tools.find_repos(p1,search_depth = config['index_depth'],exclude=exclude)

        if args.user=='all':
            for username,token in config['github_accounts'].items():
                print('User: ',username)
                git_tools.retrieve_nonlocal_repos(git_list,clean_path(config['clone_path']), user=username,token = token,exclude_remote=config['exclude_remote'],verbose = args.verbose)    
        elif args.user == 'new':        
            user,token,save = new_user()
            git_tools.retrieve_nonlocal_repos(git_list,clean_path(config['clone_path']),user,token,exclude_remote=config['exclude_remote'],verbose = args.verbose)    
            if save:
                try:
                    config['github_accounts'][user]=token
                except KeyError:
                    config['github_accounts']={}
                    config['github_accounts'][user]=token
        else:
            token = config['github_accounts'][args.user]
            git_tools.retrieve_nonlocal_repos(git_list,clean_path(config['clone_path']), user=args.user,token = token,exclude_remote=config['exclude_remote'],verbose = args.verbose)    

    elif (args.command == 'list-github'):
        all_users = {}
        if args.user=='all':
            for user,token in config['github_accounts'].items():
                git_list,owners,owner_repo_dict = git_tools.list_remote_repos(user=user,token = token)
                all_users[user]=owner_repo_dict
                
        elif args.user == 'new':        
            user,token,save = new_user()
            git_list,owners,owner_repo_dict = git_tools.list_remote_repos(user=user,token = token)
            all_users[user]=owner_repo_dict

            if save:
                try:
                    config['github_accounts'][user]=token
                except KeyError:
                    config['github_accounts']={}
                    config['github_accounts'][user]=token
        else:
            token = config['github_accounts'][args.user]
            git_list,owners,owner_repo_dict = git_tools.list_remote_repos(user=args.user,token = token)
            all_users[args.user]=owner_repo_dict
        
        print(yaml.dump(all_users))

    elif (args.command == 'list-github-nonlocal'):

        git_list = git_tools.find_repos(p1,search_depth = config['index_depth'],exclude=exclude)

        # all_users = {}
        all_repos = []
        if args.user=='all':
            for user,token in config['github_accounts'].items():
                local_git_list,owners,owner_repo_dict = git_tools.list_nonlocal_repos(git_list,user=user,token = token)
                # all_users[user]=owner_repo_dict
                all_repos.extend(local_git_list)
        elif args.user == 'new':        
            user,token,save = new_user()
            local_git_list,owners,owner_repo_dict = git_tools.list_nonlocal_repos(git_list,user=user,token = token)
            # all_users[user]=owner_repo_dict
            all_repos.extend(local_git_list)

            if save:
                try:
                    config['github_accounts'][user]=token
                except KeyError:
                    config['github_accounts']={}
                    config['github_accounts'][user]=token
        else:
            token = config['github_accounts'][args.user]
            local_git_list,owners,owner_repo_dict = git_tools.list_nonlocal_repos(git_list,user=args.user,token = token)
            # all_users[args.user]=owner_repo_dict
            all_repos.extend(local_git_list)

        all_repos = [git_tools.remote_url_from_ssh_address(item) for item in all_repos]        
        print(yaml.dump(all_repos))

    elif args.command == 'reset':

        git_list = git_tools.index_git_list(p1,not args.no_index,index_cache_path,config['index_depth'],exclude_mod)

        git_tools.reset_branches(git_list)

    elif args.command == 'list-active-branch':

        git_list = git_tools.index_git_list(p1,not args.no_index,index_cache_path,config['index_depth'],exclude_mod)

        current_branch = git_tools.get_current_branch(git_list)
        s = yaml.dump(current_branch)
        print(s)
    
    elif args.command == 'index':
    
        git_list = git_tools.index_git_list(p1,True,index_cache_path,config['index_depth'],exclude_mod)
        if args.verbose:
            s = yaml.dump(git_list)
            print(s)

    elif args.command == 'list':
        git_list = git_tools.index_git_list(p1,True,index_cache_path,config['index_depth'],exclude_mod)
        s = yaml.dump(git_list)
        print(s)

    elif args.command == 'exclude':
    
        path = clean_path(os.curdir)
        config['exclude_local'].append(path)
        print(path)
    
    else:
        raise(Exception('command does not exist'))        
        
    if args.config_f is None:
        config_save_path = personal_config_path
        if not os.path.exists(personal_config_folder):
            os.makedirs(personal_config_folder)
    else:
        config_save_path = args.config_f
    
    config_save_path = clean_path(config_save_path)
    
    with open(config_save_path,'w') as f:
        yaml.dump(config,f)
    
