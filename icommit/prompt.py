# -*- coding: utf-8 -*-
# @File : prompt.py
# @Author : r.yang
# @Date : Wed Mar 15 17:02:18 2023
# @Description :


from dataclasses import dataclass


@dataclass
class Prompt:
    summarize: str
    classify: str

    locale_set: bool = False
    diff_set: bool = False
    max_char_set: bool = False


PROMPT_SET = [
    Prompt(
        summarize="Write an insightful, succinct but concise Git commit message in a complete sentence in present tense for the following diff without prefacing it with anything, you'd better start it with an appropriate emoji according to your message",
        classify="""The following code diff can be classified to 8 types:
1. feat: A new feature, such as the add or remove of functions/classes
2. fix: A bug fix, some typo fixes or small logic fixes
3. docs: Documentation only changes, including files like *.md *.adoc *.org, etc.
4. style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
5. refactor: A code change that neither fixes a bug nor adds a feature
6. perf: A code change that improves performance
7. test: Adding missing or correcting existing tests, must including filenames start or end with 'test'
8. chore: Changes to the build process or auxiliary tools and libraries such as documentation generation, dockerfile, gitlab ci, github workflow, etc.

please return the best type according to the diff, you must give me **one** word only""",
    ),
]


def with_locale(prompt: Prompt, locale: str = 'en'):
    if prompt.locale_set:
        return prompt

    prompt.summarize += f', the response must be in the language {locale}'
    return prompt


def with_max_char(prompt: Prompt, max_char: int):
    if prompt.max_char_set:
        return prompt

    prompt.summarize += f', no more than {max_char} characters'
    return prompt


def with_diff(prompt: Prompt, diff: str):
    if prompt.diff_set:
        return prompt

    prompt.summarize += f'\n\n{diff}'
    prompt.classify += f'\n\n{diff}'
    return prompt
