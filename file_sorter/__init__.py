"""
File Sorter - An intelligent file organization tool
"""

__version__ = "1.0.0"
__author__ = "File Sorter Team"
__license__ = "MIT"

from .core import FileSorter
from .config import Config

__all__ = ["FileSorter", "Config"]
