import os
import shutil
import datetime

# 1. Define workspace root and backup directory
workspace_root = os.getcwd()
backup_dir = os.path.join(workspace_root, 'backup')

# Create backup directory if it doesn't exist
os.makedirs(backup_dir, exist_ok=True)

# 2. Create timestamped backup destination
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
dest_dir = os.path.join(backup_dir, timestamp)
os.makedirs(dest_dir)

print(f"Backup directory created: {dest_dir}")

# 3. Copy files and directories (Rule 3.2)
errors = []
for item in os.listdir(workspace_root):
    source_path = os.path.join(workspace_root, item)
    dest_path = os.path.join(dest_dir, item)
    
    # Exclude the backup directory itself from being copied
    if item == 'backup' or item == 'tmp_backup.py':
        continue
        
    try:
        if os.path.isdir(source_path):
            shutil.copytree(source_path, dest_path, symlinks=True, ignore_dangling_symlinks=True)
        else:
            shutil.copy2(source_path, dest_path)
    except Exception as e:
        errors.append(f"Could not copy {source_path}: {e}")

if not errors:
    print("Workspace content copied to backup directory.")
else:
    print("Backup process encountered errors:")
    for error in errors:
        print(error)


# 4. Prune old backups (Rule 3.4)
try:
    backups = sorted([d for d in os.listdir(backup_dir) if os.path.isdir(os.path.join(backup_dir, d))])
    if len(backups) > 10:
        num_to_delete = len(backups) - 10
        print(f"Found {len(backups)} backups, which is more than 10. Deleting {num_to_delete} oldest backup(s).")
        for i in range(num_to_delete):
            dir_to_delete = os.path.join(backup_dir, backups[i])
            print(f"Deleting old backup: {dir_to_delete}")
            shutil.rmtree(dir_to_delete)
    else:
        print(f"Found {len(backups)} backups. No pruning needed.")
except Exception as e:
    print(f"Error during backup pruning: {e}")


print("Backup script finished.")
