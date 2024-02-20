from setuptools import setup, find_packages

with open("README.md", "r") as f:
    desc = f.read()

setup(
    name="cli_chronicler",
    version="0.6.1",
    packages=find_packages(),
    entry_points={"console_scripts": ["punch = cli_chronicler:main"]},
    description="A command line app for keeping track of project/work times.",
    long_description=desc,
    long_description_content_type="text/markdown"
)
