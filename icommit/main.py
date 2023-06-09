# -*- coding: utf-8 -*-
# @File : main.py
# @Author : r.yang
# @Date : Wed Mar 15 16:27:23 2023
# @Description : icommit main

from pathlib import Path

import typer
from rich import print

from icommit.git_tool import commit, get_diff
from icommit.model import classify, summarize
from icommit.prompt import new_prompt_set, with_diff, with_locale, with_max_char, with_summary

app = typer.Typer()
HOME_DIR = Path.home()
PROJECT_NAME = 'icommit'
MAX_DIFF_LEN = 1000


@app.command()
def set(key: str = typer.Option(...), proxy: str = typer.Option('')):
    config_dir = HOME_DIR / '.config' / PROJECT_NAME
    config_dir.mkdir(exist_ok=True, parents=True)

    with open(config_dir / 'key', 'w') as f:
        f.write(key.strip())

    if proxy:
        with open(config_dir / 'proxy', 'w') as f:
            f.write(proxy.strip())

    print(f'your key/proxy is saved to {config_dir}')


def _get_key():
    key_path = HOME_DIR / '.config' / PROJECT_NAME / 'key'
    if not key_path.exists():
        print('ERROR: key not set, please run `icommit set-key ${your key} firstly`')
        return ''
    return open(key_path).read().strip()


def _get_proxy():
    proxy_path = HOME_DIR / '.config' / PROJECT_NAME / 'proxy'
    if not proxy_path.exists():
        return ''
    return open(proxy_path).read().strip()


@app.command()
def get():

    key = _get_key()
    proxy = _get_proxy()

    if not key:
        return

    print(f'your key   is: {key}')
    print(f'your proxy is: {proxy}')


@app.command()
def diff():
    print(get_diff(MAX_DIFF_LEN))


from rich.prompt import Prompt

MESSAGE_TYPES = [
    'feat',
    'fix',
    'docs',
    'style',
    'refactor',
    'perf',
    'test',
    'chore',
]


@app.command()
def run(locale: str = typer.Option('en'), max_char: int = typer.Option(20)):
    message_type = Prompt.ask(
        'commit message type: ', choices=['auto'] + MESSAGE_TYPES, default='auto'
    )
    diff = get_diff(MAX_DIFF_LEN)
    if not diff.strip():
        print('ERROR: empty diff, use `git add` to make changes staged')
        return
    key = _get_key()
    if not key:
        return

    cnt = 0
    while 1:
        for prompt in new_prompt_set():
            if locale:
                prompt = with_locale(prompt, locale)
            prompt = with_max_char(prompt, max_char)
            prompt = with_diff(prompt, diff)
            message = summarize(prompt, api_key=key, proxy=_get_proxy(),)

            if message_type == 'auto':
                new_message_type = classify(
                    with_summary(prompt, message), api_key=key, proxy=_get_proxy()
                )
                print(f'message type generated by gpt: {new_message_type}')
            else:
                new_message_type = message_type

            if len(new_message_type.split(' ')) == 1:
                message = f'{new_message_type}: {message}'

            print(f'commit message: \n\n\t\t{message}\n')

            accept = typer.confirm('ok?', default=True)
            if accept:
                commit(message)
                print('message commited! use `git commit --amend` to edit it')
                return
            cnt += 1


if __name__ == '__main__':
    app()
