from setuptools import find_packages, setup

import re

with open('requirements.txt', 'r') as file:
    requirements = [re.sub('\n','',i) for i in file]

setup(
    name='sqlIntuitive',
    package_dir={"":"src"},
    packages=find_packages(where="src"),
    version='0.2.0',
    description='Library for easy and intuitive use of database systems.',
    author="Moritz Bauer",
    license="MIT",
    install_requires=requirements,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests'
)
