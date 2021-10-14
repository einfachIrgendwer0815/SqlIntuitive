from setuptools import find_packages, setup

import re
import json

with open('requirements.txt', 'r') as file:
    requirements = [re.sub('\n','',i) for i in file]

with open('version.json', 'r') as file:
    version = json.load(file)['version']

setup(
    name='sqlIntuitive',
    python_requires='>=3.8',
    package_dir={"":"src"},
    packages=find_packages(where="src"),
    version=version,
    description='Library for easy and intuitive use of database systems.',
    author="Moritz Bauer",
    license="MIT",
    install_requires=requirements,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests'
)
