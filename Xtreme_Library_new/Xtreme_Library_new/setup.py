from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='xtreme_library',
    version='0.1',
    packages=find_packages(),
    author='Syed',
    description='Automation helper for Excel, video capture and consolidation',
    long_description=long_description,
    long_description_content_type='text/markdown',
)