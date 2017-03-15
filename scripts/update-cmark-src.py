#!/usr/bin/env python3

import os
import shutil
import argparse
import subprocess


DEST_DIR = os.path.abspath("paka/cmark/cmark_src/")

KEEP = {"LICENSE"}


def run(args, cwd):
    subprocess.check_call(args, cwd=cwd)


def copy(src_dir, dest_dir, *, filename):
    shutil.copyfile(
        os.path.join(src_dir, filename),
        os.path.join(dest_dir, filename))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmark_repo")
    args = parser.parse_args()

    repo = args.cmark_repo
    build_dir = os.path.join(repo, "build")

    # Build sources.
    os.mkdir(build_dir)
    run(["cmake", ".."], cwd=build_dir)

    # Clean DEST_DIR.
    for filename in os.listdir(DEST_DIR):
        if filename not in KEEP:
            os.unlink(os.path.join(DEST_DIR, filename))

    # Copy files from repo/src/.
    src_dir = os.path.join(repo, "src")
    for filename in os.listdir(src_dir):
        copy(src_dir, DEST_DIR, filename=filename)

    build_src_dir = os.path.join(build_dir, "src")

    # Copy config.h from repo/build/src/.
    copy(build_src_dir, DEST_DIR, filename="config.h")

    # Copy cmark_* from repo/build/src/.
    for filename in os.listdir(build_src_dir):
        if filename.startswith("cmark_"):
            copy(build_src_dir, DEST_DIR, filename=filename)


if __name__ == "__main__":
    main()
