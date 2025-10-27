"""
Configuration management for File Sorter
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional


class Config:
    """Configuration class for managing file sorting rules and settings"""
    
    DEFAULT_CATEGORIES = {
        "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
        "Pictures": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico", ".tiff", ".webp"],
        "Music": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"],
        "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx", ".doc", ".xls", ".ppt", ".odt", ".rtf"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
        "Code": [".py", ".js", ".java", ".cpp", ".c", ".h", ".cs", ".php", ".rb", ".go", ".rs", ".html", ".css"],
        "Executables": [".exe", ".msi", ".app", ".deb", ".rpm", ".dmg"],
        "Spreadsheets": [".csv", ".xlsx", ".xls", ".ods"],
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration
        
        Args:
            config_path: Path to custom configuration file (JSON)
        """
        self.config_path = config_path
        self.categories = self.DEFAULT_CATEGORIES.copy()
        
        if config_path and os.path.exists(config_path):
            self.load_config(config_path)
    
    def load_config(self, config_path: str) -> None:
        """Load configuration from JSON file
        
        Args:
            config_path: Path to configuration file
        """
        try:
            with open(config_path, 'r') as f:
                custom_config = json.load(f)
                if 'categories' in custom_config:
                    self.categories.update(custom_config['categories'])
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config from {config_path}: {e}")
    
    def save_config(self, config_path: str) -> None:
        """Save current configuration to JSON file
        
        Args:
            config_path: Path where to save configuration
        """
        try:
            with open(config_path, 'w') as f:
                json.dump({'categories': self.categories}, f, indent=2)
        except IOError as e:
            print(f"Error: Could not save config to {config_path}: {e}")
    
    def get_categories(self) -> Dict[str, List[str]]:
        """Get all file categories and their extensions
        
        Returns:
            Dictionary mapping category names to lists of file extensions
        """
        return self.categories.copy()
    
    def add_category(self, category_name: str, extensions: List[str]) -> None:
        """Add a new category or update existing one
        
        Args:
            category_name: Name of the category
            extensions: List of file extensions (e.g., ['.mp4', '.avi'])
        """
        self.categories[category_name] = extensions
    
    def remove_category(self, category_name: str) -> None:
        """Remove a category
        
        Args:
            category_name: Name of the category to remove
        """
        if category_name in self.categories:
            del self.categories[category_name]
    
    def get_category_for_extension(self, extension: str) -> Optional[str]:
        """Get category name for a given file extension
        
        Args:
            extension: File extension (e.g., '.mp4')
            
        Returns:
            Category name or None if not found
        """
        extension = extension.lower()
        for category, extensions in self.categories.items():
            if extension in extensions:
                return category
        return None
