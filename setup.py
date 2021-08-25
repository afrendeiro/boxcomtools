#! /usr/bin/env python

"""
Installer script for the ``boxcomtools`` package.
"""

from setuptools import setup, find_packages
from pathlib import Path


def parse_requirements(req_file):
    """Parse requirements.txt files."""
    reqs = open(req_file).read().strip().split("\n")
    reqs = [r for r in reqs if not r.startswith("#")]
    return [r for r in reqs if ("#egg=" not in r) and (r != "")]


# Requirements
reqs = parse_requirements("requirements.txt")

# Description
long_description = open("README.md").read()


# setup
setup(
    name="boxcomtools",
    packages=find_packages(),
    use_scm_version={
        "write_to": "boxcomtools/_version.py",
        "write_to_template": 'version = __version__ = "{version}"\n',
    },
    # entry_points={
    #     "console_scripts": [
    #         "boxcomtools = boxcomtools.cli:main",
    #     ]
    # },
    description="Tools to work with the Box.com SDK.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 3 - Alpha",
        "Typing :: Typed",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        # "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    keywords=",".join(
        [
            # "mass spectrometry",
        ]
    ),
    url="https://github.com/afrendeiro/boxcomtools",
    project_urls={
        "Bug Tracker": "https://github.com/afrendeiro/boxcomtools/issues",
        # "Documentation": "https://boxcomtools.readthedocs.io",
        "Source Code": "https://github.com/afrendeiro/boxcomtools",
    },
    author=u"Andre Rendeiro",
    author_email="andre.rendeiro@pm.me",
    license="GPL3",
    setup_requires=["setuptools_scm"],
    install_requires=reqs,
    # tests_require=reqs["dev"],
    # extras_require={k: v for k, v in reqs.items() if k not in ["base", "dev"]},
    # package_data={"boxcomtools": ["config/*.yaml", "templates/*.html", "_models/*"]},
    # data_files=[("requirements", reqs.values())],
)
