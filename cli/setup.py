#!/usr/bin/env python
"""The setup script."""

from setuptools import setup, find_packages
from pathlib import Path


here = Path(__file__).parent
repo_root = here/".."


with open(repo_root/"README.md") as readme_file:
    readme = readme_file.read()

requirements = [
    "Click>=6.0",
    "requests"
]

setup_requirements = []

setup(
    author="Chris Lunsford",
    author_email="chrlunsf@cisco.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    description="Command Line Interface for the Rapid ZTP App.",
    entry_points={
        "console_scripts": [
            "ztpcli=ztpcli.cli:main",
        ],
    },
    install_requires=requirements,
    license="Cisco Sample Code License, Version 1.1",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="ztpcli",
    name="ztpcli",
    packages=find_packages(include=["ztpcli"]),
    setup_requires=setup_requirements,
    url="https://github.com/CiscoSE/rapid-ztp",
    version="0.1.0",
    zip_safe=False,
)
