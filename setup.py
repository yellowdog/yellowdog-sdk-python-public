import os

from setuptools import setup, find_packages

version = {}
with open("src/yellowdog_client/_version.py") as fp:
    exec(fp.read(), version)

master_version_split = version['__version__'].split(".")
master_version = "%s.%s.%s" % (master_version_split[0], master_version_split[1], master_version_split[2])

branch_name = os.environ.get("BRANCH_NAME", "dev")
revision = os.environ.get("REVISION", "1")
branch = ".dev"
if branch_name == "dev" or branch_name.startswith("/feature") or branch_name.startswith("feature"):
    branch = ".dev"
if branch_name == "test":
    branch = ".a"
if branch_name == "staging":
    branch = ".rc"
if branch_name == "master":
    branch = ""
    revision = ""

final_version = '%s%s%s' % (master_version, branch, revision)

# Hack to update the module version which the docs build later depends on
with open("src/yellowdog_client/_version.py", "w") as fp:
    fp.write(f"__version__ = '{final_version}'\n")

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='yellowdog-sdk',
    version=final_version,
    description='Client SDK for the YellowDog Platform',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="YellowDog Limited",
    author_email="support@yellowdog.co",
    url="https://yellowdog.co/",
    project_urls={
        'Source': 'https://github.com/yellowdog/yellowdog-sdk-python'
    },
    license='Apache Software License, version 2.0',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "jsons==1.4.0",
        "requests==2.25.1",
        "python-dispatch==0.1.31",
        "sseclient==0.0.24",
        "cancel-token==0.1.5",
        "isodate==0.6.0"
        "futures;python_version<'3.2'",
        "enum;python_version<'3.4'",
    ],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'License :: OSI Approved :: Apache Software License'
    ]
)
