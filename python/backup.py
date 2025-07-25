import os
import tarfile
import logging
from datetime import datetime
import subprocess

# Configure logging
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_xdg_user_dir(dirname: str) -> str:
    """Get the path to a XDG user directory (e.g., Documents, Downloads) respecting localization."""
    try:
        path = subprocess.check_output(['xdg-user-dir', dirname], text=True).strip()
        return path
    except Exception as e:
        logging.warning(f'Could not get XDG user dir for {dirname}: {e}')
        return os.path.join(os.path.expanduser("~"), dirname)

def get_important_files(list_file='backup_list.txt') -> list[str]:
    """Read a list of important files from a specified file.
    Each line in the file should contain a path to a file or directory.
    Returns a list of absolute paths."""
    important_files = []
    xdg_dirs = {
        "XDG_DOCUMENTS_DIR": get_xdg_user_dir("DOCUMENTS"),
        "XDG_DOWNLOAD_DIR": get_xdg_user_dir("DOWNLOAD"),
        # Add more as needed
    }
    try:
        with open(list_file, 'r') as f:
            for line in f:
                path = line.strip()
                if path:
                    # Replace XDG placeholders
                    for key, value in xdg_dirs.items():
                        if key in path:
                            path = path.replace(key, value)
                    path = os.path.expanduser(path)
                    important_files.append(path)
    except Exception as e:
        logging.error(f'Error reading list file: {e}')
    return important_files

def create_backup_tar(backup_dir, list_file='backup_list.txt') -> None:
    """Create a tar.gz backup of important files listed in the specified file.
    The backup will be stored in the specified backup directory."""
    os.makedirs(backup_dir, exist_ok=True)
    backup_name = f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.tar.gz'
    backup_path = os.path.join(backup_dir, backup_name)
    important_files = get_important_files(list_file)
    logging.info('Starting backup process...')
    try:
        with tarfile.open(backup_path, "w:gz") as tar:
            for file_path in important_files:
                if os.path.exists(file_path):
                    # Store with absolute path in archive
                    arcname = file_path if file_path.startswith("/") else "/" + file_path
                    tar.add(file_path, arcname=arcname)
                    logging.info(f'Added to backup: {file_path}')
                else:
                    logging.warning(f'File or directory does not exist: {file_path}')
        logging.info(f'Backup tarball created at: {backup_path}')
    except Exception as e:
        logging.error(f'Error creating backup tarball: {e}')

def main() -> None:
    """Main function to create a backup."""
    backup_dir = os.path.expanduser("~/backups")
    create_backup_tar(backup_dir)

if __name__ == '__main__':
    main()