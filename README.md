# File Sorter 📁

An intelligent, feature-rich file organization tool that automatically sorts your files into categorized folders. Built with Python and designed for ease of use with a beautiful command-line interface.

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

### Core Functionality
- **Smart File Categorization**: Automatically organizes files into categories:
  - 🎥 **Videos**: .mp4, .mkv, .avi, .mov, .wmv, .flv, .webm
  - 🖼️ **Pictures**: .jpg, .jpeg, .png, .gif, .bmp, .svg, .ico, .tiff, .webp
  - 🎵 **Music**: .mp3, .wav, .flac, .aac, .ogg, .m4a, .wma
  - 📄 **Documents**: .pdf, .docx, .txt, .pptx, .xlsx, .doc, .xls, .ppt, .odt, .rtf
  - 📦 **Archives**: .zip, .rar, .7z, .tar, .gz, .bz2, .xz
  - 💻 **Code**: .py, .js, .java, .cpp, .c, .h, .cs, .php, .rb, .go, .rs, .html, .css
  - ⚙️ **Executables**: .exe, .msi, .app, .deb, .rpm, .dmg
  - 📊 **Spreadsheets**: .csv, .xlsx, .xls, .ods

### Advanced Features
- ⏪ **Undo Functionality**: Restore files to their original locations
- 🔍 **Duplicate Detection**: Find duplicate files based on content hash
- 📅 **Date-based Organization**: Organize files by modification date within categories
- 🎯 **Dry Run Mode**: Preview what will be sorted before making changes
- 🔧 **Custom Configuration**: Create custom file categories and rules
- 📊 **Statistics**: View file distribution across categories
- 🎨 **Beautiful CLI**: Rich, colorful terminal interface with progress indicators
- 🔄 **Multiple Duplicate Strategies**: Skip, rename, or replace duplicate files

## 📦 Installation

### Option 1: Install from Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/Tony-Stone-Code/python_script_automation-file_sorter.git
cd python_script_automation-file_sorter

# Install the package
pip install -e .
```

### Option 2: Install from PyPI (Coming Soon)

```bash
pip install file-sorter
```

### Option 3: Install Dependencies Only

```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

After installation, you can use the `file-sorter` command from anywhere in your terminal:

```bash
# Sort files in your Downloads folder (default)
file-sorter

# Sort files in a specific directory
file-sorter -s /path/to/your/directory

# Preview what would be sorted (dry run)
file-sorter --dry-run

# Show statistics about files
file-sorter --stats
```

## 📖 Usage

### Basic Commands

```bash
# Sort files in Downloads folder
file-sorter

# Sort files in a custom directory
file-sorter --source /path/to/directory

# Preview changes without moving files
file-sorter --dry-run

# Organize files by date within categories
file-sorter --organize-by-date

# Show file statistics
file-sorter --stats

# Find duplicate files
file-sorter --find-duplicates
```

### Advanced Options

```bash
# Undo last 5 operations
file-sorter --undo 5

# Use custom configuration file
file-sorter --config my_config.json

# Handle duplicates by renaming (default)
file-sorter --duplicate-strategy rename

# Handle duplicates by skipping
file-sorter --duplicate-strategy skip

# Handle duplicates by replacing
file-sorter --duplicate-strategy replace

# Quiet mode (suppress output)
file-sorter --quiet
```

### Command-Line Options

| Option | Description |
|--------|-------------|
| `-s, --source DIR` | Source directory to sort (default: ~/Downloads) |
| `-c, --config FILE` | Path to custom configuration JSON file |
| `--dry-run` | Preview what would be done without moving files |
| `--organize-by-date` | Organize files by modification date within categories |
| `--duplicate-strategy {skip,rename,replace}` | How to handle duplicate files (default: rename) |
| `--undo COUNT` | Undo last COUNT file operations |
| `--stats` | Show statistics about files in source directory |
| `--find-duplicates` | Find and report duplicate files |
| `-q, --quiet` | Suppress verbose output |
| `--version` | Show version information |

## ⚙️ Configuration

You can create a custom configuration file to define your own file categories:

```json
{
  "categories": {
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Pictures": [".jpg", ".jpeg", ".png", ".gif"],
    "Music": [".mp3", ".wav", ".flac"],
    "Documents": [".pdf", ".docx", ".txt"],
    "MyCustomCategory": [".custom", ".ext"]
  }
}
```

Then use it with:

```bash
file-sorter --config my_config.json
```

## 🎯 Use Cases

### Organize Downloads Folder
```bash
file-sorter
```

### Clean Up Project Directory
```bash
file-sorter --source ~/Projects/messy-folder --dry-run
file-sorter --source ~/Projects/messy-folder
```

### Archive Files by Date
```bash
file-sorter --organize-by-date --source ~/Documents
```

### Find and Remove Duplicates
```bash
file-sorter --find-duplicates --source ~/Pictures
```

## 🔧 Development

### Running from Source

```bash
# Clone the repository
git clone https://github.com/Tony-Stone-Code/python_script_automation-file_sorter.git
cd python_script_automation-file_sorter

# Install in development mode
pip install -e .

# Run the application
file-sorter
```

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=file_sorter
```

## 📝 Legacy Script

The original `files_sorter.py` script is still available for backwards compatibility:

```bash
python3 files_sorter.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Inspired by the need for better file organization

## 🐛 Bug Reports

If you encounter any issues, please report them on the [GitHub Issues](https://github.com/Tony-Stone-Code/python_script_automation-file_sorter/issues) page.

## ⭐ Support

If you find this tool useful, please consider giving it a star on GitHub!



