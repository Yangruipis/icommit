# -*- coding: utf-8 -*-
# @File : git.py
# @Author : r.yang
# @Date : Wed Mar 15 16:46:17 2023
# @Description : git command

import subprocess


def get_diff(cut_off: int) -> str:
    entire_diff = get_entire_diff()
    if len(entire_diff) < cut_off:
        return entire_diff

    return get_short_diff()


def get_entire_diff() -> str:
    arguments = [
        'git',
        '--no-pager',
        'diff',
        '--staged',
        '--ignore-space-change',
        '--ignore-all-space',
        '--ignore-blank-lines',
    ]
    diff_process = subprocess.run(arguments, capture_output=True, text=True)
    diff_process.check_returncode()
    return diff_process.stdout.strip()


def get_short_diff() -> str:
    arguments = [
        'git',
        '--no-pager',
        'diff',
        '--staged',
        '--ignore-space-change',
        '--ignore-all-space',
        '--ignore-blank-lines',
        '--stat',
    ]
    diff_process = subprocess.run(arguments, capture_output=True, text=True)
    diff_process.check_returncode()
    return diff_process.stdout.strip()


def commit(message: str):
    if not message:
        return
    return subprocess.run(['git', 'commit', '--message', message]).returncode
