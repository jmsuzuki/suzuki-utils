# setup.py

from setuptools import setup, find_packages

setup(
    name="suzuki_utils",
    version="0.1.0",
    description="utils project",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Mitchell Suzuki",
    author_email="mitchell.suzuki@gmail.com",
    url="https://github.com/jmsuzuki/suzuki-utils",
    packages=find_packages(),
    install_requires=[],
)
