from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="adac-blockchain",
    version="0.1.0",
    author="ADAC Team",
    description="ADAC Blockchain Implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BurcUnalan/ADAC-Blockchain-Complete",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)