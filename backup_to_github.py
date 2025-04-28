import os
import subprocess
import shutil

# Set up the repository paths
source_repo_path = '/home/runner/work/MEMEPEDIA-CONTENT/MEMEPEDIA-CONTENT'
backup_repo_path = '/tmp/memepedia_backup'
backup_repo_url = 'https://github.com/MagicDippyEgg/MEMEPEDIA-BACKUP.git'
gh_token = os.getenv('GH_TOKEN')

# Function to run git commands
def run_git_command(command, cwd=None):
    result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Running command: {' '.join(command)}")
    print(f"Command output: {result.stdout.decode('utf-8')}")
    print(f"Command error: {result.stderr.decode('utf-8')}")
    return result

# Clone the backup repository
def clone_backup_repo():
    if os.path.exists(backup_repo_path):
        print(f"Backup repo already exists at {backup_repo_path}. Pulling latest changes...")
        result = run_git_command(['git', 'pull'], cwd=backup_repo_path)
        if result.returncode != 0:
            raise Exception(f"Error pulling backup repository: {result.stderr.decode('utf-8')}")
    else:
        print("Cloning backup repository...")
        result = run_git_command(['git', 'clone', backup_repo_url, backup_repo_path])
        if result.returncode != 0:
            raise Exception(f"Error cloning backup repository: {result.stderr.decode('utf-8')}")

# Clone the source repository
def clone_source_repo():
    if os.path.exists(source_repo_path):
        print(f"Source repository already exists at {source_repo_path}. Skipping clone.")
    else:
        print("Cloning source repository...")
        result = run_git_command(['git', 'clone', 'https://github.com/MagicDippyEgg/MEMEPEDIA-CONTENT.git', source_repo_path])
        if result.returncode != 0:
            raise Exception(f"Error cloning source repository: {result.stderr.decode('utf-8')}")

# Set Git user name and email
def set_git_user_identity():
    print("Setting Git user name and email for commits...")
    run_git_command(['git', 'config', 'user.name', 'MagicDippyEgg'])
    run_git_command(['git', 'config', 'user.email', 'magicdippyegg@gmail.com'])

# Push changes to the backup repository
def push_to_backup():
    print("Checking for changes...")
    
    # Stage all changes to ensure Git tracks them
    result = run_git_command(['git', 'add', '.'], cwd=backup_repo_path)
    if result.returncode != 0:
        raise Exception(f"Error adding files: {result.stderr.decode('utf-8')}")
    
    # Commit changes
    commit_result = run_git_command(['git', 'commit', '-m', 'Backup commit from GitHub Actions'], cwd=backup_repo_path)
    if commit_result.returncode != 0:
        print("No changes to commit.")
    else:
        # Push the changes to the backup repository
        push_result = run_git_command(['git', 'push', 'origin', 'main'], cwd=backup_repo_path)
        if push_result.returncode == 0:
            print("Backup successfully pushed.")
        else:
            print(f"Error during push: {push_result.stderr.decode('utf-8')}")

# Main process
def main():
    try:
        # Clone the source repo if it doesn't exist
        clone_source_repo()
        
        # Clone the backup repository
        clone_backup_repo()
        
        # Remove the backup folder if it exists
        if os.path.exists(backup_repo_path):
            print(f"Deleting existing backup directory at {backup_repo_path}...")
            shutil.rmtree(backup_repo_path)
        
        # Now, copy the source repository to the backup path
        print(f"Copying source files to {backup_repo_path}...")
        shutil.copytree(source_repo_path, backup_repo_path)
        
        # Verify the files were copied
        if os.path.exists(backup_repo_path):
            print("Files successfully copied.")
        else:
            print("Error: Files were not copied to the backup directory.")
        
        # Change to the backup repo directory to check for changes
        os.chdir(backup_repo_path)
        
        # Initialize git in case the repo is new
        result = run_git_command(['git', 'init'], cwd=backup_repo_path)
        if result.returncode != 0:
            raise Exception(f"Error initializing git in backup repo: {result.stderr.decode('utf-8')}")
        
        # Fetch the latest changes from the backup repo to ensure we're synced
        fetch_result = run_git_command(['git', 'fetch'], cwd=backup_repo_path)
        if fetch_result.returncode != 0:
            raise Exception(f"Error fetching latest changes from backup repo: {fetch_result.stderr.decode('utf-8')}")
        
        # Set Git user identity for commits
        set_git_user_identity()
        
        # Add all files explicitly to Git
        result = run_git_command(['git', 'add', '.'], cwd=backup_repo_path)
        
        # Commit and push the changes if any are detected
        push_to_backup()
        
    except Exception as e:
        print(f"Error during backup: {e}")
        exit(1)

if __name__ == "__main__":
    main()
