from setuptools import setup, find_packages

with open("README.md", "r") as f:
    desc = f.read()

setup(
    name="cli_chronicler",
    version="0.5.1",
    packages=find_packages(),
    entry_points={"console_scripts": ["punch = cli_chronicler:main"]},
    long_description=desc,
    long_description_content_type="text/markdown"
)
