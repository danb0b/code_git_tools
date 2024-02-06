---
title: README
---

## Introduction

gitman uses ssh namespacing in order to differentiate between different github usernames and ssh keys.  This requires the ability to modify the .ssh/config account for your user.  In windows this has traditionally been difficult but doable.

## Installation

The easiest way to install git manager is to use pip

```bash
pip install git_manage
```

This will install the git_manage package as well as the ```gitman``` script

## Configuration

These instructions assume you may have more than one github account.  For each github account,

1. Create an API key
    1. go to account settings --> developer settings --> personal access tokens
        1. select tokens(classic) from the left hand panel
        1. generate new token (classic) for general use
        1. set to the expiration of your preference.  
            1. check the following
                1. repo(checks all)
        1. copy the resulting api key and save somewhere safe.

1. Create a SSH key for each account
    1. go to account settings --> ssh and gpg keys
    1. create a new ssh key.

        Create one locally, with a passphrase, save it to your .ssh folder or somewhere expected, and then copy the key in to the box

1. edit your .ssh/config file

    for each github user, create a new entry:

        ```
        Host <username1>.github.com
            HostName github.com
            User git
            IdentityFile /path/to/username1/key/file
            PreferredAuthentications publickey 
        ```

        ```
        Host <username2>.github.com
            HostName github.com
            User git
            IdentityFile /path/to/username2/key/file
            PreferredAuthentications publickey 
        ```

1. Set up a new config file



## todo

* [ ] save repos into user/project/repo structure rather than project/repo so you can have duplicate repos.
* [ ] investigate switching from git hard reset to git fast forward.
* [ ] 