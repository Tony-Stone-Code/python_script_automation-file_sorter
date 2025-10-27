from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="file-sorter",
    version="1.0.0",
    author="File Sorter Team",
    description="An intelligent file organization tool with CLI and advanced features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tony-Stone-Code/python_script_automation-file_sorter",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        "rich>=13.0.0",
    ],
    extras_require={
        "watch": ["watchdog>=3.0.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "file-sorter=file_sorter.cli:main",
        ],
    },
    keywords=["file", "organizer", "sorter", "automation", "cli"],
)
