#!/usr/bin/env python

import os
import shutil
import sys
from pathlib import Path

if len(sys.argv) < 4:
    print("Usage: install.py <project_name> <author> <email> [<description>]")
    exit(1)

source_dir = Path(__file__).parent / "PROJECT"

target_dir = Path(sys.argv[1].lower().replace(" ", "_").replace("-", "_").replace(".", "_"))
if target_dir.exists():
    print(f'"{target_dir}" exists. Not installing.')
    exit(2)

project = target_dir.name
author = sys.argv[2]
email = sys.argv[3]
if len(sys.argv) > 4:
    description = " ".join(sys.argv[4:])
else:
    description = project
print(f'Creating project "{project}"')
print(f' with description "{description}"')
print(f' author is "{author}"')
print(f' with email "{email}"')
print()
print(f'Installing to "{target_dir}"')
shutil.copytree(source_dir, target_dir)


def rename():
    for subdir, dirs, files in os.walk(target_dir):
        for name in dirs + files:
            if "PROJECT" in name:
                src = os.path.join(subdir, name)
                tgt = src.replace("PROJECT", project, 1)
                print(f"Rename {src} to {tgt}")
                shutil.move(src, tgt)
                return True
    return False


while rename():
    pass

for subdir, dirs, files in os.walk(target_dir):
    for name in files:
        src = os.path.join(subdir, name)
        with open(src) as f:
            lines = f.read()
        newlines = (
            lines.replace("PROJECT", project)
            .replace("AUTHOR", author)
            .replace("EMAIL", email)
            .replace("DESCRIPTION", description)
        )
        if newlines != lines:
            tgt = src
            print(f"Updating {tgt}")
            with open(tgt, "w") as f:
                f.write(newlines)
print("Done!")
