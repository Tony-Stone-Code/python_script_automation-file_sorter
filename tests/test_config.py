"""
Tests for File Sorter configuration
"""

import os
import json
import tempfile
import unittest
from file_sorter.config import Config


class TestConfig(unittest.TestCase):
    """Test cases for Config class"""
    
    def test_default_categories(self):
        """Test that default categories are loaded"""
        config = Config()
        categories = config.get_categories()
        
        self.assertIn("Videos", categories)
        self.assertIn("Pictures", categories)
        self.assertIn("Music", categories)
        self.assertIn("Documents", categories)
    
    def test_get_category_for_extension(self):
        """Test getting category for file extension"""
        config = Config()
        
        self.assertEqual(config.get_category_for_extension(".mp4"), "Videos")
        self.assertEqual(config.get_category_for_extension(".jpg"), "Pictures")
        self.assertEqual(config.get_category_for_extension(".mp3"), "Music")
        self.assertEqual(config.get_category_for_extension(".pdf"), "Documents")
        self.assertIsNone(config.get_category_for_extension(".unknown"))
    
    def test_add_category(self):
        """Test adding a new category"""
        config = Config()
        config.add_category("TestCategory", [".test", ".tst"])
        
        categories = config.get_categories()
        self.assertIn("TestCategory", categories)
        self.assertEqual(categories["TestCategory"], [".test", ".tst"])
        self.assertEqual(config.get_category_for_extension(".test"), "TestCategory")
    
    def test_remove_category(self):
        """Test removing a category"""
        config = Config()
        config.remove_category("Videos")
        
        categories = config.get_categories()
        self.assertNotIn("Videos", categories)
    
    def test_load_config_from_file(self):
        """Test loading configuration from JSON file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "categories": {
                    "CustomCategory": [".custom"]
                }
            }, f)
            config_file = f.name
        
        try:
            config = Config(config_file)
            categories = config.get_categories()
            
            # Should have both default and custom categories
            self.assertIn("Videos", categories)
            self.assertIn("CustomCategory", categories)
            self.assertEqual(config.get_category_for_extension(".custom"), "CustomCategory")
        finally:
            os.unlink(config_file)
    
    def test_save_config(self):
        """Test saving configuration to file"""
        config = Config()
        config.add_category("SavedCategory", [".saved"])
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config_file = f.name
        
        try:
            config.save_config(config_file)
            
            # Load it back
            with open(config_file, 'r') as f:
                saved_config = json.load(f)
            
            self.assertIn("categories", saved_config)
            self.assertIn("SavedCategory", saved_config["categories"])
        finally:
            os.unlink(config_file)


if __name__ == '__main__':
    unittest.main()
