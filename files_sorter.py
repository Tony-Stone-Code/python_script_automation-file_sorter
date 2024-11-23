import os
import shutil

# Define the source directory (Downloads folder)
source_dir = os.path.join(os.path.expanduser("~"), "Downloads")

# Define target directories
target_dirs = {
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Pictures": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Music": [".mp3", ".wav", ".flac", ".aac"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"]
}

# Create target directories if they don't exist
for folder in target_dirs.keys():
    folder_path = os.path.join(source_dir, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Function to sort files
def sort_files():
    for filename in os.listdir(source_dir):
        # Get the file extension
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        # Check which category the file belongs to
        for folder, extensions in target_dirs.items():
            if ext in extensions:
                # Move the file to the appropriate folder
                shutil.move(os.path.join(source_dir, filename), os.path.join(source_dir, folder, filename))
                print(f'Moved: {filename} to {folder}')
                break

if __name__ == "__main__":
    sort_files()