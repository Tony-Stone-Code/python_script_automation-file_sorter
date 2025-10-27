"""
Core file sorting functionality
"""

import os
import shutil
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from .config import Config


class FileSorter:
    """Main file sorting class with enhanced features"""
    
    def __init__(self, source_dir: str, config: Optional[Config] = None, 
                 create_subdirs: bool = True, history_file: str = "file_sorter_history.json"):
        """Initialize FileSorter
        
        Args:
            source_dir: Source directory to sort files from
            config: Configuration object (uses default if None)
            create_subdirs: Whether to create category subdirectories
            history_file: Path to history file for undo functionality
        """
        self.source_dir = os.path.abspath(os.path.expanduser(source_dir))
        self.config = config or Config()
        self.create_subdirs = create_subdirs
        self.history_file = history_file
        self.history: List[Dict] = []
        self.load_history()
        
        if not os.path.exists(self.source_dir):
            raise ValueError(f"Source directory does not exist: {self.source_dir}")
    
    def load_history(self) -> None:
        """Load operation history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.history = []
    
    def save_history(self) -> None:
        """Save operation history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save history: {e}")
    
    def _ensure_directories_exist(self) -> None:
        """Create category directories if they don't exist"""
        if self.create_subdirs:
            for category in self.config.get_categories().keys():
                folder_path = os.path.join(self.source_dir, category)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
    
    def _get_file_hash(self, filepath: str) -> str:
        """Calculate MD5 hash of a file
        
        Args:
            filepath: Path to the file
            
        Returns:
            MD5 hash as hex string
        """
        hash_md5 = hashlib.md5()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except IOError:
            return ""
    
    def _handle_duplicate(self, source: str, destination: str, 
                         duplicate_strategy: str = "skip") -> Optional[str]:
        """Handle duplicate files
        
        Args:
            source: Source file path
            destination: Destination file path
            duplicate_strategy: How to handle duplicates ('skip', 'rename', 'replace')
            
        Returns:
            Final destination path or None if skipped
        """
        if not os.path.exists(destination):
            return destination
        
        if duplicate_strategy == "skip":
            return None
        elif duplicate_strategy == "replace":
            os.remove(destination)
            return destination
        elif duplicate_strategy == "rename":
            base, ext = os.path.splitext(destination)
            counter = 1
            while os.path.exists(destination):
                destination = f"{base}_{counter}{ext}"
                counter += 1
            return destination
        
        return destination
    
    def sort_files(self, dry_run: bool = False, duplicate_strategy: str = "rename",
                   organize_by_date: bool = False, verbose: bool = True) -> Dict[str, int]:
        """Sort files in the source directory
        
        Args:
            dry_run: If True, only preview what would be done
            duplicate_strategy: How to handle duplicates ('skip', 'rename', 'replace')
            organize_by_date: Organize files by modification date within categories
            verbose: Print detailed information
            
        Returns:
            Dictionary with statistics (moved, skipped, errors)
        """
        self._ensure_directories_exist()
        
        stats = {"moved": 0, "skipped": 0, "errors": 0}
        operations = []
        
        try:
            items = os.listdir(self.source_dir)
        except OSError as e:
            print(f"Error reading directory: {e}")
            return stats
        
        for filename in items:
            source_path = os.path.join(self.source_dir, filename)
            
            # Skip directories and the history file
            if os.path.isdir(source_path) or filename == os.path.basename(self.history_file):
                continue
            
            # Get file extension
            _, ext = os.path.splitext(filename)
            ext = ext.lower()
            
            # Find appropriate category
            category = self.config.get_category_for_extension(ext)
            if not category:
                stats["skipped"] += 1
                continue
            
            # Determine destination
            if organize_by_date:
                mod_time = datetime.fromtimestamp(os.path.getmtime(source_path))
                date_folder = mod_time.strftime("%Y-%m")
                dest_dir = os.path.join(self.source_dir, category, date_folder)
            else:
                dest_dir = os.path.join(self.source_dir, category)
            
            dest_path = os.path.join(dest_dir, filename)
            
            # Handle duplicates
            final_dest = self._handle_duplicate(source_path, dest_path, duplicate_strategy)
            
            if final_dest is None:
                if verbose:
                    print(f"Skipped (duplicate): {filename}")
                stats["skipped"] += 1
                continue
            
            # Execute or preview
            if dry_run:
                print(f"[DRY RUN] Would move: {filename} -> {os.path.relpath(final_dest, self.source_dir)}")
                stats["moved"] += 1
            else:
                try:
                    # Create destination directory if needed
                    os.makedirs(os.path.dirname(final_dest), exist_ok=True)
                    
                    # Move file
                    shutil.move(source_path, final_dest)
                    
                    if verbose:
                        print(f"Moved: {filename} -> {os.path.relpath(final_dest, self.source_dir)}")
                    
                    # Record operation
                    operations.append({
                        "timestamp": datetime.now().isoformat(),
                        "source": source_path,
                        "destination": final_dest,
                        "filename": filename,
                        "category": category
                    })
                    
                    stats["moved"] += 1
                except (OSError, shutil.Error) as e:
                    if verbose:
                        print(f"Error moving {filename}: {e}")
                    stats["errors"] += 1
        
        # Save history
        if operations and not dry_run:
            self.history.extend(operations)
            self.save_history()
        
        return stats
    
    def undo_last_operation(self, count: int = 1, verbose: bool = True) -> int:
        """Undo last file sorting operations
        
        Args:
            count: Number of operations to undo
            verbose: Print detailed information
            
        Returns:
            Number of files restored
        """
        restored = 0
        
        for _ in range(min(count, len(self.history))):
            if not self.history:
                break
            
            operation = self.history.pop()
            
            try:
                if os.path.exists(operation["destination"]):
                    # Restore to original location
                    shutil.move(operation["destination"], operation["source"])
                    if verbose:
                        print(f"Restored: {operation['filename']} to original location")
                    restored += 1
                else:
                    if verbose:
                        print(f"Cannot restore {operation['filename']}: file not found")
            except (OSError, shutil.Error) as e:
                if verbose:
                    print(f"Error restoring {operation['filename']}: {e}")
        
        self.save_history()
        return restored
    
    def get_statistics(self) -> Dict[str, int]:
        """Get statistics about files in source directory
        
        Returns:
            Dictionary with file counts per category
        """
        stats: Dict[str, int] = {"Uncategorized": 0}
        
        try:
            items = os.listdir(self.source_dir)
        except OSError:
            return stats
        
        for filename in items:
            filepath = os.path.join(self.source_dir, filename)
            
            if os.path.isdir(filepath):
                continue
            
            _, ext = os.path.splitext(filename)
            ext = ext.lower()
            
            category = self.config.get_category_for_extension(ext)
            if category:
                stats[category] = stats.get(category, 0) + 1
            else:
                stats["Uncategorized"] += 1
        
        return stats
    
    def find_duplicates(self, verbose: bool = True) -> Dict[str, List[str]]:
        """Find duplicate files in source directory based on content hash
        
        Args:
            verbose: Print detailed information
            
        Returns:
            Dictionary mapping file hashes to lists of file paths
        """
        hash_map: Dict[str, List[str]] = {}
        
        try:
            items = os.listdir(self.source_dir)
        except OSError:
            return {}
        
        for filename in items:
            filepath = os.path.join(self.source_dir, filename)
            
            if os.path.isdir(filepath):
                continue
            
            file_hash = self._get_file_hash(filepath)
            if file_hash:
                if file_hash not in hash_map:
                    hash_map[file_hash] = []
                hash_map[file_hash].append(filepath)
        
        # Filter to only duplicates
        duplicates = {h: files for h, files in hash_map.items() if len(files) > 1}
        
        if verbose and duplicates:
            print(f"\nFound {len(duplicates)} sets of duplicate files:")
            for file_hash, files in duplicates.items():
                print(f"\nHash {file_hash[:8]}...:")
                for f in files:
                    print(f"  - {os.path.basename(f)}")
        
        return duplicates
