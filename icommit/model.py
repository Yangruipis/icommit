# -*- coding: utf-8 -*-
# @File : openai.py
# @Author : r.yang
# @Date : Wed Mar 15 17:18:05 2023
# @Description :

import requests

from icommit.prompt import Prompt


def ask(
    content: str,
    api_key: str,
    timeout: int = 30,
    model: str = 'gpt-3.5-turbo',
    proxy: str = '',
    sys_prompt: str = 'You are ChatGPT, a large language model trained by OpenAI. Respond conversationally',
):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    data = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': sys_prompt,},
            {'role': 'user', 'content': content},
        ],
        'user': 'user',
    }

    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json=data,
        timeout=timeout,
        proxies={'http': proxy, 'https': proxy} if proxy else None,
    )

    response.raise_for_status()
    return response.json()['choices'][0]['message']['content'].lower().strip().strip('."')


def summarize(
    prompt: 'Prompt', **kwargs,
):
    return ask(prompt.summarize, **kwargs)


def classify(
    prompt: 'Prompt', **kwargs,
):
    return ask(prompt.classify, sys_prompt='you are a classifier', **kwargs).split(':')[0]
