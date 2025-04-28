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

# Push changes to the backup repository
def push_to_backup():
    print("Checking for changes...")
    # Check for changes in the backup repo
    result = run_git_command(['git', 'status', '--porcelain'], cwd=backup_repo_path)
    
    if result.stdout:
        print("Changes detected, committing and pushing...")
        # Stage the changes explicitly
        run_git_command(['git', 'add', '.'], cwd=backup_repo_path)
        
        # Commit the changes
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
    else:
        print("No changes detected in the source repository.")

# Main process
def main():
    try:
        # Clone the source repo if it doesn't exist
        clone_source_repo()
        
        # Clone the backup repository
        clone_backup_repo()
        
        # Delete existing backup folder and copy new files
        print(f"Copying files from {source_repo_path} to {backup_repo_path}...")
        
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
        
        # Check for changes and push the changes to the backup repository
        push_to_backup()

    except Exception as e:
        print(f"Error during backup: {e}")
        exit(1)

if __name__ == "__main__":
    main()
