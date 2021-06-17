# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 20:18:03 2019

@author: danaukes
"""
import os
import git_manage.git_tools as git_tools
import argparse
import yaml

def clean_path(path_in):
    path_out = os.path.normpath(os.path.abspath(os.path.expanduser(path_in)))
    return path_out


if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('command',metavar='command',type=str,help='command', default = '')
    parser.add_argument('--config',dest='config_f',default = None)
    parser.add_argument('--token',dest='token',default = None)
    parser.add_argument('-f','--force-index',dest='force_index',action='store_true', default = False)
    
    args = parser.parse_args()
    
    if args.config_f:
        with open(args.config_f) as f:
            config = yaml.load(f,Loader=yaml.Loader)
    else:
        config = None
    # print(config)

    p1 = clean_path(config['index_location'])

    exclude = config['exclude_local']
    exclude = [clean_path(item) for item in exclude]

    exclude_mod = exclude[:]
    exclude_mod.append(clean_path(config['archive_path']))

    index_cache_path = clean_path(config['index_cache'])
        
    if ((args.command == 'index') or args.force_index or (not os.path.exists(index_cache_path))):
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
        print('pull')
        # git_list = git_tools.find_repos(p1,search_depth = config['index_depth'],exclude=exclude_mod)
        git_list = git_tools.fetch(git_list)
        git_tools.check_unmatched(git_list)

    elif args.command == 'status':
        print('status')
        
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
        
    elif args.command == 'branch-status':
        print('branch')
        # git_list = git_tools.find_repos(p1,search_depth = config['index_depth'],exclude=exclude_mod)
        git_tools.check_unmatched(git_list)

        
    elif args.command == 'clone':
        print('clone')
        # git_list = git_tools.find_repos(p1,search_depth = config['index_depth'],exclude=exclude_mod)
        git_tools.retrieve_nonlocal_repos(git_list,repo_path=config['clone_path'], exclude_remote=['config.exclude_remote'],token = args.token)    
        
    elif args.command == 'reset':
        print('reset')

        #git_list = git_tools.find_repos(p1,search_depth = config.index_depth,exclude=exclude_mod)
        git_tools.reset_branches(git_list)

    elif args.command == 'index':
        pass
    else:
        raise KeyError('that argument cannot be found')