#!/usr/bin/env python

import os
import shutil
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: install.py <project_name>")
    exit(1)

source_dir = Path(__file__).parent / "PROJECT"

project = sys.argv[1]
target_dir = Path() / project

if target_dir.exists():
    print(f"\"{target_dir}\" exists. Not installing.")
    exit(2)

print(f"Installing to \"{target_dir}\"")
shutil.copytree(source_dir, target_dir)

def rename():
    for subdir, dirs, files in os.walk(target_dir):
        for name in dirs + files:
            if "PROJECT" in name:
                src = name
                tgt = name.replace("PROJECT", project, 1)
                print(f"Rename {src} to {tgt}")
                shutil.move(src, tgt)
                return True
    return False

while rename():
    pass
