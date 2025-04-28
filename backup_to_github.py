import os
import subprocess

# Backup repository details
backup_repo = "git@github.com:MagicDippyEgg/MEMEPEDIA-BACKUP.git"
source_repo = "https://github.com/MagicDippyEgg/MEMEPEDIA-CONTENT.git"
token = os.getenv("GH_TOKEN")

# Directory for cloning the source repo
backup_dir = "/tmp/memepedia_backup"

# Clone the source repo
def clone_repo():
    try:
        print("Cloning source repository...")
        subprocess.run(["git", "clone", source_repo, backup_dir], check=True)
        print("Source repository cloned successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        raise

# Push to backup repo
def push_to_backup():
    try:
        print("Pushing changes to backup repository...")
        # Change to the backup repo directory
        os.chdir(backup_dir)
        
        # Set up remote origin with the backup repo
        subprocess.run(["git", "remote", "add", "backup", backup_repo], check=True)
        
        # Set up Git config
        subprocess.run(["git", "config", "user.name", "GitHub Actions"], check=True)
        subprocess.run(["git", "config", "user.email", "actions@github.com"], check=True)
        
        # Add all files, commit, and push
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Backup commit from GitHub Actions"], check=True)
        subprocess.run(["git", "push", "backup", "main"], check=True)
        
        print("Backup to GitHub repository successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error during backup: {e}")
        raise

if __name__ == "__main__":
    clone_repo()
    push_to_backup()
