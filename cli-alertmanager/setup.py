#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import find_packages, setup


requirements = [
    "loguru==0.7.2",
    "boto3==1.36.18",
    "python-dotenv",
]

test_requirements = [
    "pytest>=6.0",
]

dev_requirements = [
    "flake8",
    "pytest-cov",
]


setup(
    name="cli-alertmanager",
    version="1.0.0",
    author="SystemFrame",
    author_email="systemframe@example.com",
    description="CLI tool for managing Alertmanager alerts and sessions",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "cli-alertmanager=cli.send:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
