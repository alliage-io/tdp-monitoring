#!/usr/bin/env python3
# Copyright 2022 TOSIT.IO",
# SPDX-License-Identifier: Apache-2.0"
import re, sys, os
import subprocess
from git import Repo
from termcolor import colored
from tdp_utils import tdp_banner, find_file_path
from ansiblelint.__main__ import _run_cli_entrypoint

def linter():
    try:
        repo = Repo('.', search_parent_directories=True)
        root = os.path.basename(repo.git.rev_parse("--show-toplevel"))
        tdp_banner(root,'Running ansible-lint...')
    except:
        print(colored("This does not seem to be a git repository",'yellow'))
        root = os.path.basename(os.getcwd())
    collection_path=find_file_path('ansible_collections')
    if collection_path is None:
        print(colored("Can't find collection path",'yellow'))
    my_env = os.environ.copy()
    my_env["ANSIBLE_COLLECTIONS_PATH"] = collection_path
    command = sys.executable+ " -m ansiblelint "+' '.join(sys.argv[1:])
    ret = subprocess.run(command, env = my_env, shell = True).returncode
    return ret

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(linter())
