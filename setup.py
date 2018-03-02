from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Servo-IRCBot',
    version='1.0.0',
    description='An IRC bot written in Twisted.',
    url='https://github.com/AWilliams17/Servo-IRCBot/',
    author='Austin Williams',
    author_email='awilliams17411@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Framework :: Twisted'
        'License :: Freeware'
        'Topic :: Communications :: Chat :: Internet Relay Chat'
        'Programming Language :: Python :: 2.7',
    ],

    keywords='ircbot twisted twisted-ircbot irc',
    packages=find_packages(exclude=['tests']),

    install_requires=['twisted', 'BeautifulSoup', 'requests'],

    entry_points={
        'console_scripts': [
            'servo=bin.servo:main',
        ],
    },

    project_urls={
        'Bug Reports': 'https://github.com/AWilliams17/Servo-IRCBot/issues',
        'Source': 'https://github.com/AWilliams17/Servo-IRCBot/',
    },
)
