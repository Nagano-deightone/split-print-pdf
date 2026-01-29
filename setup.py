"""
Setup configuration for split-print package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="split-print",
    version="0.1.0",
    description="Split tall PDFs into printable A4-sized pages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/split-print",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pypdf>=3.0.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "split-print=split_print.cli:main",
            "batch-split-print=split_print.batch_cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="pdf split print a4 converter",
)
