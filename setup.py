import pathlib

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="fluentfs",
    version="0.4.0",
    description="Functional and fluent interface for filesystem interactions",
    packages=find_packages(),
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/uhasker/fluentfs",
    author="uhasker",
    author_email="uhasker@protonmail.com",
    license="MIT",
)
