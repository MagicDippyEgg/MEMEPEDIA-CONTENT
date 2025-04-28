import os
import shutil
from github import Github

# Replace this with your GitHub repository details
GITHUB_TOKEN = os.getenv('GH_TOKEN')  # GitHub token set as an environment variable
REPO_NAME = 'MagicDippyEgg/MEMEPEDIA-BACKUP'  # Example: 'MagicDippyEgg/MEMEPEDIA-BACKUP'
BRANCH_NAME = 'main'

# Initialize GitHub API client
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# Define the backup folder (replace with your directory to backup)
BACKUP_DIR = '/path/to/your/files'  # For example: '/home/runner/work/MEMEPEDIA-CONTENT'

# Function to upload files to GitHub repository
def upload_files():
    for filename in os.listdir(BACKUP_DIR):
        file_path = os.path.join(BACKUP_DIR, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
                try:
                    # This will create or update the file on the repository
                    repo.create_file(
                        f'backup/{filename}',  # Path where files will be saved in GitHub repo
                        'Backup of files',  # Commit message
                        content,
                        branch=BRANCH_NAME
                    )
                    print(f'File {filename} uploaded successfully.')
                except Exception as e:
                    print(f'Failed to upload {filename}: {e}')

if __name__ == '__main__':
    upload_files()
