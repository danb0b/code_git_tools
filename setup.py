# -*- coding: utf-8 -*-
'''
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
'''

from setuptools import setup
import sys
import shutil

shutil.rmtree("build", ignore_errors=True)
shutil.rmtree("dist", ignore_errors=True)
shutil.rmtree('git_manage.egg-info', ignore_errors=True)


packages = []
packages.append('git_manage')
#packages.append('git_manage.scripts')

package_data = {}
package_data['git_manage'] = []
# package_data['git_manage'].append('gitman')
package_data['git_manage'].append('support/config.yaml')

setup_kwargs = {}
setup_kwargs['name']='git_manage'
setup_kwargs['version']='0.0.9'
setup_kwargs['classifiers']=['Programming Language :: Python','Programming Language :: Python :: 3']   
setup_kwargs['description']='Git Management Tools are a collection of tools for making it easier to manage 100+ local repos'
setup_kwargs['author']='Dan Aukes'
setup_kwargs['author_email']='danaukes@danaukes.com'
setup_kwargs['url']='https://github.com/danb0b/code_git_tools'
setup_kwargs['license']='MIT'
setup_kwargs['packages']=packages
setup_kwargs['package_dir']={'git_manage' : 'python/git_manage'}
setup_kwargs['package_data'] = package_data
setup_kwargs['install_requires']=['pygithub','gitpython','pyyaml']
setup_kwargs['scripts'] = ['bash/gitman']
  
setup(**setup_kwargs)
