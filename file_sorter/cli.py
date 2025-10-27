"""
Command-line interface for File Sorter
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    rprint = print

from .core import FileSorter
from .config import Config

try:
    from .watch import WatchMode
    WATCH_AVAILABLE = True
except ImportError:
    WATCH_AVAILABLE = False


class CLI:
    """Command-line interface handler"""
    
    def __init__(self):
        """Initialize CLI"""
        self.console = Console() if RICH_AVAILABLE else None
    
    def print_banner(self):
        """Print application banner"""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║                    FILE SORTER v1.0                       ║
║          Intelligent File Organization Tool               ║
╚═══════════════════════════════════════════════════════════╝
        """
        
        if RICH_AVAILABLE:
            self.console.print(Panel(banner, style="bold blue"))
        else:
            print(banner)
    
    def print_statistics(self, stats: dict, title: str = "Statistics"):
        """Print statistics in a nice table format
        
        Args:
            stats: Dictionary with statistics
            title: Table title
        """
        if RICH_AVAILABLE:
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("Category", style="cyan")
            table.add_column("Count", justify="right", style="green")
            
            for category, count in sorted(stats.items()):
                if count > 0:
                    table.add_row(category, str(count))
            
            self.console.print(table)
        else:
            print(f"\n{title}")
            print("-" * 40)
            for category, count in sorted(stats.items()):
                if count > 0:
                    print(f"{category:20s}: {count:>5d}")
            print("-" * 40)
    
    def create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser
        
        Returns:
            Configured ArgumentParser
        """
        parser = argparse.ArgumentParser(
            description="File Sorter - Organize your files intelligently",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Sort files in Downloads folder
  file-sorter
  
  # Sort files in a specific directory
  file-sorter -s /path/to/directory
  
  # Preview what would be sorted (dry run)
  file-sorter --dry-run
  
  # Sort with date-based organization
  file-sorter --organize-by-date
  
  # Undo last 5 operations
  file-sorter --undo 5
  
  # Show statistics about files
  file-sorter --stats
  
  # Find duplicate files
  file-sorter --find-duplicates
  
  # Watch directory and auto-sort new files
  file-sorter --watch
  
  # Use custom configuration
  file-sorter --config my_config.json
            """
        )
        
        parser.add_argument(
            '-s', '--source',
            default=os.path.join(os.path.expanduser("~"), "Downloads"),
            help='Source directory to sort (default: ~/Downloads)'
        )
        
        parser.add_argument(
            '-c', '--config',
            help='Path to custom configuration JSON file'
        )
        
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview what would be done without actually moving files'
        )
        
        parser.add_argument(
            '--organize-by-date',
            action='store_true',
            help='Organize files by modification date within categories'
        )
        
        parser.add_argument(
            '--duplicate-strategy',
            choices=['skip', 'rename', 'replace'],
            default='rename',
            help='How to handle duplicate files (default: rename)'
        )
        
        parser.add_argument(
            '--watch',
            action='store_true',
            help='Watch directory and automatically sort new files (requires watchdog package)'
        )
        
        parser.add_argument(
            '--undo',
            type=int,
            metavar='COUNT',
            help='Undo last COUNT file operations'
        )
        
        parser.add_argument(
            '--stats',
            action='store_true',
            help='Show statistics about files in source directory'
        )
        
        parser.add_argument(
            '--find-duplicates',
            action='store_true',
            help='Find and report duplicate files (based on content hash)'
        )
        
        parser.add_argument(
            '-q', '--quiet',
            action='store_true',
            help='Suppress verbose output'
        )
        
        parser.add_argument(
            '--version',
            action='version',
            version='File Sorter v1.0.0'
        )
        
        return parser
    
    def run(self, args: Optional[list] = None) -> int:
        """Run the CLI application
        
        Args:
            args: Command-line arguments (uses sys.argv if None)
            
        Returns:
            Exit code (0 for success, non-zero for error)
        """
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)
        
        # Print banner unless quiet mode
        if not parsed_args.quiet:
            self.print_banner()
        
        # Load configuration
        config = Config(parsed_args.config) if parsed_args.config else Config()
        
        # Initialize sorter
        try:
            sorter = FileSorter(parsed_args.source, config)
        except ValueError as e:
            if RICH_AVAILABLE:
                self.console.print(f"[bold red]Error:[/bold red] {e}")
            else:
                print(f"Error: {e}")
            return 1
        
        verbose = not parsed_args.quiet
        
        # Handle undo operation
        if parsed_args.undo:
            if RICH_AVAILABLE:
                self.console.print(f"[yellow]Undoing last {parsed_args.undo} operations...[/yellow]")
            else:
                print(f"Undoing last {parsed_args.undo} operations...")
            
            restored = sorter.undo_last_operation(parsed_args.undo, verbose)
            
            if RICH_AVAILABLE:
                self.console.print(f"[green]✓[/green] Restored {restored} files")
            else:
                print(f"✓ Restored {restored} files")
            
            return 0
        
        # Handle statistics display
        if parsed_args.stats:
            stats = sorter.get_statistics()
            self.print_statistics(stats, "Files in Source Directory")
            return 0
        
        # Handle duplicate finding
        if parsed_args.find_duplicates:
            if RICH_AVAILABLE:
                self.console.print("[yellow]Searching for duplicate files...[/yellow]")
            else:
                print("Searching for duplicate files...")
            
            duplicates = sorter.find_duplicates(verbose)
            
            if not duplicates:
                if RICH_AVAILABLE:
                    self.console.print("[green]No duplicate files found![/green]")
                else:
                    print("No duplicate files found!")
            
            return 0
        
        # Handle watch mode
        if parsed_args.watch:
            if not WATCH_AVAILABLE:
                if RICH_AVAILABLE:
                    self.console.print("[bold red]Error:[/bold red] Watch mode requires 'watchdog' package")
                    self.console.print("[yellow]Install it with:[/yellow] pip install watchdog")
                else:
                    print("Error: Watch mode requires 'watchdog' package")
                    print("Install it with: pip install watchdog")
                return 1
            
            watch_mode = WatchMode(sorter, verbose)
            watch_mode.start()
            return 0
        
        # Perform file sorting
        if parsed_args.dry_run and verbose:
            if RICH_AVAILABLE:
                self.console.print("[yellow]DRY RUN MODE - No files will be moved[/yellow]\n")
            else:
                print("DRY RUN MODE - No files will be moved\n")
        
        if verbose:
            if RICH_AVAILABLE:
                self.console.print(f"[cyan]Source directory:[/cyan] {parsed_args.source}")
                if parsed_args.organize_by_date:
                    self.console.print("[cyan]Organization:[/cyan] By date within categories")
                self.console.print(f"[cyan]Duplicate strategy:[/cyan] {parsed_args.duplicate_strategy}\n")
            else:
                print(f"Source directory: {parsed_args.source}")
                if parsed_args.organize_by_date:
                    print("Organization: By date within categories")
                print(f"Duplicate strategy: {parsed_args.duplicate_strategy}\n")
        
        # Sort files
        stats = sorter.sort_files(
            dry_run=parsed_args.dry_run,
            duplicate_strategy=parsed_args.duplicate_strategy,
            organize_by_date=parsed_args.organize_by_date,
            verbose=verbose
        )
        
        # Print summary
        if verbose:
            self.print_statistics(stats, "Summary")
            
            if not parsed_args.dry_run and stats["moved"] > 0:
                if RICH_AVAILABLE:
                    self.console.print("\n[green]✓[/green] Files sorted successfully!")
                    self.console.print(f"[dim]Use 'file-sorter --undo {stats['moved']}' to undo this operation[/dim]")
                else:
                    print("\n✓ Files sorted successfully!")
                    print(f"Use 'file-sorter --undo {stats['moved']}' to undo this operation")
        
        return 0


def main():
    """Main entry point for the CLI application"""
    cli = CLI()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()
