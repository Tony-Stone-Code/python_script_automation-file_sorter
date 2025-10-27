"""
Watch mode functionality for File Sorter
"""

import os
import time
from typing import Optional
from .core import FileSorter
from .config import Config

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileCreatedEvent
    WATCHDOG_AVAILABLE = True
    
    class FileCreatedHandler(FileSystemEventHandler):
        """Handler for file creation events"""
        
        def __init__(self, sorter: FileSorter, verbose: bool = True):
            """Initialize handler
            
            Args:
                sorter: FileSorter instance
                verbose: Whether to print verbose output
            """
            super().__init__()
            self.sorter = sorter
            self.verbose = verbose
        
        def on_created(self, event):
            """Handle file creation event
            
            Args:
                event: File system event
            """
            if isinstance(event, FileCreatedEvent) and not event.is_directory:
                # Wait a bit to ensure file is fully written
                time.sleep(0.5)
                
                filename = os.path.basename(event.src_path)
                _, ext = os.path.splitext(filename)
                
                category = self.sorter.config.get_category_for_extension(ext.lower())
                if category:
                    if self.verbose:
                        print(f"New file detected: {filename}")
                    
                    # Sort just this file
                    stats = self.sorter.sort_files(verbose=self.verbose)
    
    
    class WatchMode:
        """Watch mode for continuous file monitoring"""
        
        def __init__(self, sorter: FileSorter, verbose: bool = True):
            """Initialize watch mode
            
            Args:
                sorter: FileSorter instance
                verbose: Whether to print verbose output
            """
            self.sorter = sorter
            self.verbose = verbose
            self.observer: Optional[Observer] = None
        
        def start(self):
            """Start watching the directory"""
            event_handler = FileCreatedHandler(self.sorter, self.verbose)
            self.observer = Observer()
            self.observer.schedule(event_handler, self.sorter.source_dir, recursive=False)
            self.observer.start()
            
            if self.verbose:
                print(f"Watching {self.sorter.source_dir} for new files...")
                print("Press Ctrl+C to stop")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop()
        
        def stop(self):
            """Stop watching the directory"""
            if self.observer:
                self.observer.stop()
                self.observer.join()
                if self.verbose:
                    print("\nStopped watching.")

except ImportError:
    WATCHDOG_AVAILABLE = False
    FileCreatedHandler = None
    WatchMode = None

