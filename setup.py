from setuptools import setup

setup(
    name='ghcli',
    version='0.1',
    description='GitHub command line tools',
    url='http://github.com/larsks/ghcli',
    author='Lars Kellogg-Stedman',
    author_email='lars@oddbit.com',
    license='GPLv3',
    packages=['ghcli'],
    entry_points={
        'console_scripts': [
            'gh=ghcli.main:github',
        ]
    }
)
