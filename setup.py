from setuptools import find_packages, setup

setup(
    name='icommit',
    description='',
    packages=find_packages(),
    author='Yangruipis',
    entry_points="""
    [console_scripts]
    icommit=icommit.main:app
    """,
    install_requires=['typer', 'rich', 'requests'],
    version='0.0.1',
    python_requires='>=3.7',
    url='https://github.com/Yangruipis/icommit',
)
