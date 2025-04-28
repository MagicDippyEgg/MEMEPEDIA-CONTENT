import os
import subprocess
import shutil

# Define repository paths and settings
source_repo_path = "/home/runner/work/MEMEPEDIA-CONTENT/MEMEPEDIA-CONTENT"
backup_repo_path = "/tmp/memepedia_backup"
backup_repo_url = "https://github.com/MagicDippyEgg/MEMEPEDIA-BACKUP.git"
git_user_name = "MagicDippyEgg"
git_user_email = "magicdippyegg@gmail.com"

# Function to clone the backup repository
def clone_backup_repo():
    if os.path.exists(backup_repo_path):
        print("Backup repository already exists, skipping clone.")
    else:
        print("Cloning backup repository...")
        subprocess.run(["git", "clone", backup_repo_url, backup_repo_path], check=True)

# Function to initialize the Git repository in the backup directory
def init_git_repo():
    print("Reinitializing git repository in backup...")
    subprocess.run(["git", "init"], cwd=backup_repo_path, check=True)

# Function to set the git user name and email for commits
def set_git_config():
    print("Setting Git user name and email...")
    subprocess.run(["git", "config", "user.name", git_user_name], cwd=backup_repo_path, check=True)
    subprocess.run(["git", "config", "user.email", git_user_email], cwd=backup_repo_path, check=True)

# Function to copy files from the source repository to the backup repository
def copy_files():
    print("Deleting existing backup directory...")
    if os.path.exists(backup_repo_path):
        shutil.rmtree(backup_repo_path)
    os.makedirs(backup_repo_path, exist_ok=True)

    print(f"Copying files from {source_repo_path} to {backup_repo_path}...")
    shutil.copytree(source_repo_path, backup_repo_path, dirs_exist_ok=True)
    print("Files successfully copied.")

# Function to check for changes and commit them to the backup repository
def check_and_commit_changes():
    print("Checking for changes...")
    subprocess.run(["git", "add", "-A"], cwd=backup_repo_path, check=True)  # Force add all changes (including deletions)
    result = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=backup_repo_path)
    
    if result.returncode == 0:
        print("No changes detected.")
    else:
        print("Changes detected. Committing changes...")
        subprocess.run(["git", "commit", "-m", "Backup commit from GitHub Actions"], cwd=backup_repo_path, check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=backup_repo_path, check=True)
        print("Changes committed and pushed to backup repository.")

def backup():
    # Clone the backup repository (or skip if already cloned)
    clone_backup_repo()

    # Initialize git in the backup repo and configure user details
    init_git_repo()
    set_git_config()

    # Copy files from the source repo to the backup repo
    copy_files()

    # Check for changes and commit them to the backup repo
    check_and_commit_changes()

if __name__ == "__main__":
    backup()
