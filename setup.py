import setuptools
import codecs
import os


local = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(local, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


# This gets deployed when a new release is made by github actions
VERSION = '{{VERSION_PLACEHOLDER}}'
# VERSION = '0.0.1'

# CHANGEME VARS
PACKAGE_NAME = "dark-web3-lib"
DESCRIPTION = 'dARK web3 libs'
LONG_DESCRIPTION = 'Sample project for automatic releases to PyPi'
AUTHOR_NAME = "Thiago Nóbrega"
AUTHOR_EMAIL = "thiagonobrega@gmail.com"
PROJECT_URL = "https://github.com/dark-pid/dark-web3-lib"
PROJECT_KEYWORDS = ['ARK', 'dARK', 'PID', 'web3']
# required 3rd party tools used by your package
# REQUIRED_PACKAGES = ['pandas'] # unsuser

# Read more about classifiers at https://pypi.org/classifiers/
CLASSIFIERS = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent"]

setuptools.setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    url = PROJECT_URL,
    long_description=long_description,
    long_description_content_type="text/markdown",
    # install_requires=REQUIRED_PACKAGES,
    packages=setuptools.find_packages(),
    keywords=PROJECT_KEYWORDS,
    classifiers=CLASSIFIERS,
)