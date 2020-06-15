# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 09:39:04 2018

@author: danaukes
"""

import pydevtools.git_stuff.git_tools as git_tools

if __name__ == "__main__":
    
    all_gits = git_tools.scan_github()
    
    import yaml
    with open('gits_github.yaml','w') as f:
        yaml.dump(all_gits,f)   

#    string1 = page3.content.decode(page2.encoding)
#    string2 = string1.encode('cp850','replace').decode('cp850')
#
#    with open('test.html','w') as f:
#        f.writelines(string2)
