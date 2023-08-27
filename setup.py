#!/usr/bin/env python
from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'localstack_extension_authress', 'VERSION')) as version_file:
  VERSION = version_file.read().strip()

print("Building version", VERSION)

setup(
    version = VERSION,
    keywords = ['Authorization as a service', 'Security', 'authorization', 'authorization as a service', 'authentication', 'user authentication', 'Authress', 'Authress client', 'access management', 'access management as a service', 'user security', 'localstack', 'localstack extensions', 'verified', 'verified access', 'verified permissions', 'open source policy engine', 'embedded authorization', 'batteries included authorization'],
)
