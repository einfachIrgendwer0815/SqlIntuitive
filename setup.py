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
    include_package_data=True,
    version=version,
    description='Library for easy and intuitive use of database systems.',
    long_description='Library for easy and intuitive use of database systems.',
    author="Moritz Bauer",
    url="https://www.github.com/einfachIrgendwer0815/SqlIntuitive",
    license="MIT",
    install_requires=requirements,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests'
)
