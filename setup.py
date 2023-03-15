#!/usr/bin/python
from setuptools import setup, find_namespace_packages

with open('requirements.txt', mode='r', encoding='utf-8') as file:
    REQUIREMENTS = file.readlines()

with open('README.md', mode='r', encoding='utf-8') as file:
    README = file.read()


setup(
    name='simple-cdd-yaml',
    version='0.1',
    author='Sietze van Buuren',
    author_email='s.van.buuren@gmail.com',
    packages=find_namespace_packages(include=['simple-cdd-yaml', 'simple-cdd-yaml.*']),
    python_requires=">=3.8",
    package_dir={"simple-cdd-yaml": "simple-cdd-yaml"},
    entry_points ={
        'console_scripts': [
            'simple-cdd-yaml = simple_cdd_yaml.simple_cdd_yaml:main'
        ]
    },
    url='https://github.com/swvanbuuren/simple-cdd-yaml',
    license='LICENSE',
    description='YAML recipe interpreter for Simple-CDD',
    long_description=README,
    install_requires=REQUIREMENTS,
)
