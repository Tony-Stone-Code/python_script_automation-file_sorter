"""
Tests for File Sorter core functionality
"""

import os
import shutil
import tempfile
import unittest
from file_sorter.core import FileSorter
from file_sorter.config import Config


class TestFileSorter(unittest.TestCase):
    """Test cases for FileSorter class"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.config = Config()
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_init_valid_directory(self):
        """Test initialization with valid directory"""
        sorter = FileSorter(self.test_dir, self.config)
        self.assertEqual(sorter.source_dir, os.path.abspath(self.test_dir))
    
    def test_init_invalid_directory(self):
        """Test initialization with invalid directory"""
        with self.assertRaises(ValueError):
            FileSorter("/nonexistent/directory", self.config)
    
    def test_sort_files(self):
        """Test basic file sorting"""
        # Create test files
        test_files = [
            "video.mp4",
            "image.jpg",
            "song.mp3",
            "document.pdf"
        ]
        
        for filename in test_files:
            open(os.path.join(self.test_dir, filename), 'w').close()
        
        sorter = FileSorter(self.test_dir, self.config)
        stats = sorter.sort_files(verbose=False)
        
        self.assertEqual(stats["moved"], 4)
        self.assertEqual(stats["errors"], 0)
        
        # Check that files were moved to correct directories
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Videos", "video.mp4")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Pictures", "image.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Music", "song.mp3")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "Documents", "document.pdf")))
    
    def test_dry_run(self):
        """Test dry run mode"""
        # Create test files
        test_files = ["video.mp4", "image.jpg"]
        for filename in test_files:
            open(os.path.join(self.test_dir, filename), 'w').close()
        
        sorter = FileSorter(self.test_dir, self.config)
        stats = sorter.sort_files(dry_run=True, verbose=False)
        
        self.assertEqual(stats["moved"], 2)
        
        # Files should still be in original location
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "video.mp4")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "image.jpg")))
    
    def test_duplicate_handling_rename(self):
        """Test duplicate file handling with rename strategy"""
        # Create a file and its destination
        source_file = os.path.join(self.test_dir, "video.mp4")
        open(source_file, 'w').close()
        
        videos_dir = os.path.join(self.test_dir, "Videos")
        os.makedirs(videos_dir)
        existing_file = os.path.join(videos_dir, "video.mp4")
        open(existing_file, 'w').close()
        
        sorter = FileSorter(self.test_dir, self.config)
        stats = sorter.sort_files(duplicate_strategy="rename", verbose=False)
        
        # Original should be renamed
        self.assertTrue(os.path.exists(os.path.join(videos_dir, "video_1.mp4")))
    
    def test_get_statistics(self):
        """Test getting file statistics"""
        # Create test files
        open(os.path.join(self.test_dir, "video1.mp4"), 'w').close()
        open(os.path.join(self.test_dir, "video2.mkv"), 'w').close()
        open(os.path.join(self.test_dir, "image.jpg"), 'w').close()
        
        sorter = FileSorter(self.test_dir, self.config)
        stats = sorter.get_statistics()
        
        self.assertEqual(stats.get("Videos", 0), 2)
        self.assertEqual(stats.get("Pictures", 0), 1)
    
    def test_undo_operation(self):
        """Test undo functionality"""
        # Create and sort a file
        test_file = os.path.join(self.test_dir, "video.mp4")
        open(test_file, 'w').close()
        
        sorter = FileSorter(self.test_dir, self.config)
        sorter.sort_files(verbose=False)
        
        # File should be in Videos folder
        moved_file = os.path.join(self.test_dir, "Videos", "video.mp4")
        self.assertTrue(os.path.exists(moved_file))
        self.assertFalse(os.path.exists(test_file))
        
        # Undo
        restored = sorter.undo_last_operation(count=1, verbose=False)
        self.assertEqual(restored, 1)
        
        # File should be back in original location
        self.assertTrue(os.path.exists(test_file))
        self.assertFalse(os.path.exists(moved_file))


if __name__ == '__main__':
    unittest.main()
