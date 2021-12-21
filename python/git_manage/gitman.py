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

def clean_path(path_in):
    path_out = os.path.normpath(os.path.abspath(os.path.expanduser(path_in)))
    return path_out

def makedirs(path_in):
    path = clean_path(path_in)
    if os.path.splitext(path)[1]!='':
        path = os.path.split(path)[0]
    os.makedirs(path)
    
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
    parser.add_argument('command',metavar='command',type=str,help='command', default = '')
    parser.add_argument('--config',dest='config_f',default = None)
    parser.add_argument('--token',dest='token',default = None)
    parser.add_argument('-n','--no-index',dest='no_index',action='store_true', default = False)
    parser.add_argument('-d','--debug',dest='debug',action='store_true', default = False)
    
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
    exclude_mod.append(clean_path(config['archive_path']))

    index_cache_path = clean_path(config['index_cache'])
        
    if ((args.command == 'index') or (not args.no_index) or (not os.path.exists(index_cache_path))):
        git_list = git_tools.find_repos(p1,search_depth = config['index_depth'],exclude=exclude_mod)
        with open(index_cache_path,'w') as f:
            yaml.dump(git_list,f)
        s=yaml.dump(git_list)
        if (args.command == 'index'):
            print(s)

    if ((args.command == 'list') or (not args.no_index) or (not os.path.exists(index_cache_path))):
        git_list = git_tools.find_repos(p1,search_depth = config['index_depth'],exclude=exclude_mod)
        with open(index_cache_path,'w') as f:
            yaml.dump(git_list,f)
        s=yaml.dump(git_list)
        if (args.command == 'index'):
            print(s)

    with open(index_cache_path) as f:
        git_list=yaml.load(f,Loader=yaml.Loader)

    # print('Excluded Paths:', str(exclude_mod))

    if args.command == 'pull':
        # git_list = git_tools.find_repos(p1,search_depth = config['index_depth'],exclude=exclude_mod)
        git_list = git_tools.fetch(git_list)
        git_tools.check_unmatched(git_list)

    elif args.command == 'status':
        
        # git_list = git_tools.find_repos(p1,search_depth = config['index_depth'],exclude=exclude_mod)
    
        git_list2,dirty,no_path = git_tools.check_dirty(git_list)
        print('---------')
        print('Dirty:')
        for item in dirty:
            print(item)
        print('---------')
        print('No Path:')
        for item,e in no_path:
            print(item,e)
        
    elif args.command in ['branch-status','bs','branch_status']:
        # git_list = git_tools.find_repos(p1,search_depth = config['index_depth'],exclude=exclude_mod)
        git_tools.check_unmatched(git_list)

        
    elif args.command == 'clone':
        
        def new_user():
            print('No github accounts present in config')
            user = input('username: ')
            token = input('token: ')
            save = input('save user info? (y/n)')
            save = save.lower()=='y'
            return user,token,save

        git_list = git_tools.find_repos(p1,search_depth = config['index_depth'],exclude=exclude)
        try:
            if len(config['github_accounts'])>0:
                for username,token in config['github_accounts'].items():
                    print('User: ',username)
                    git_tools.retrieve_nonlocal_repos(git_list,clean_path(config['clone_path']), user=username,token = token,exclude_remote=config['exclude_remote'])    
            else: 
                user,token,save = new_user()
                git_tools.retrieve_nonlocal_repos(git_list,clean_path(config['clone_path']),user,token,exclude_remote=config['exclude_remote'])    
                if save:
                    config['github_accounts'][user]=token
        except KeyError as e:
            user,token,save = new_user()
            git_tools.retrieve_nonlocal_repos(git_list,clean_path(config['clone_path']),user,token,exclude_remote=config['exclude_remote'])    
            if save:
                config['github_accounts']={}
                config['github_accounts'][user]=token
        
    elif args.command == 'reset':

        #git_list = git_tools.find_repos(p1,search_depth = config.index_depth,exclude=exclude_mod)
        git_tools.reset_branches(git_list)

    elif args.command == 'index':
        pass
    elif args.command == 'list':
        pass
    else:
        raise KeyError('that argument cannot be found')
        
    if args.config_f is None:
        config_save_path = personal_config_path
        if not os.path.exists(personal_config_folder):
            os.makedirs(personal_config_folder)
    else:
        config_save_path = args.config_f
    
    config_save_path = clean_path(config_save_path)
    
    with open(config_save_path,'w') as f:
        yaml.dump(config,f)
    
