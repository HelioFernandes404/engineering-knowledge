#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand
import re
import sys


root_dir = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Flask==3.1.0",
    "loguru==0.7.2",
    "boto3==1.36.18",
    "twilio==9.4.5",
    "python-dotenv",
    "memoizit[redis]",
    "sf_common @ git+ssh://git@github.com/systemframe/systemframe-common.git@0.0.1-a2e6ad5",
]

test_requirements = [
    "pytest>=6.0",
]

dev_requirements = [
    "flake8",
    "pytest-cov",
]


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def get_version(package):
    """
    Return package version as listed in `__version__` in `__init__.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


setup(
    name="webhook-glpi",
    version="1.0.0",
    author="SystemFrame",
    author_email="systemframe@example.com",
    description="Webhook para integração com o GLPI",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "webhook-glpi=webhook_glpi.app:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
