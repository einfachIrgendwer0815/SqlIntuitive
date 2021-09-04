from setuptools import find_packages, setup

setup(
    name='sqlIntuitive',
    package_dir={"":"src"},
    packages=find_packages(where="src"),
    version='0.1.0',
    description='Library for easy and intuitive use of database systems.',
    author="Moritz Bauer",
    license="MIT",
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests'
)
