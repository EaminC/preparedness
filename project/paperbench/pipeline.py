import os
import shutil
import subprocess
import tarfile

# Step 1: Run the long evaluation command first
run_command = [
    "python", "-m", "paperbench.nano.entrypoint",
    "paperbench.solver=paperbench.nano.eval:ExternalPythonCodingSolver",
    "paperbench.solver.agent_id=aisi-basic-agent-openai-dev",
    "paperbench.solver.cluster_config=alcatraz.clusters.local:LocalConfig",
    "paperbench.solver.cluster_config.image=aisi-basic-agent:latest",
    "paperbench.paper_split=debug",
    "runner.recorder=nanoeval.json_recorder:json_recorder",
    "paperbench.local_runs_dir=./env_only"
]

print("Running evaluation...")
subprocess.run(run_command, check=True)
print("Evaluation finished.")

# Step 2: Move all .tar and .tar.gz files to the group directory, delete other files
base_dir = './env_only'

# Find the first-level directory under env_only (should be only one)
for group_dir in os.listdir(base_dir):
    group_path = os.path.join(base_dir, group_dir)
    if os.path.isdir(group_path):
        # Find the second-level directory inside the group directory
        for sub_dir in os.listdir(group_path):
            sub_path = os.path.join(group_path, sub_dir)
            if os.path.isdir(sub_path):
                # Process files inside the second-level directory
                for filename in os.listdir(sub_path):
                    file_path = os.path.join(sub_path, filename)
                    if filename.endswith('.tar') or filename.endswith('.tar.gz'):
                        # Move .tar and .tar.gz files to the group_path
                        shutil.move(file_path, group_path)
                        print(f"Moved archive file: {filename}")
                    else:
                        # Delete non-tar files
                        os.remove(file_path)
                        print(f"Deleted file: {filename}")
                # After processing, delete the empty second-level directory
                shutil.rmtree(sub_path)
                print(f"Deleted subdirectory: {sub_dir}")

print("Initial cleanup completed.")

# Step 3: Further processing - keep only the latest repro tar.gz, extract and clean up
# Find all .tar.gz files inside the run group directory
tar_files = [f for f in os.listdir(group_path) if f.endswith('.tar.gz')]

# Filter for 'repro' tar.gz files
repro_files = [f for f in tar_files if 'repro' in f]
if not repro_files:
    print("No repro tar.gz file found.")
    exit(1)

# Sort repro files to find the latest one based on filename
repro_files.sort()
target_repro_tar = repro_files[-1]
print(f"Keeping repro file: {target_repro_tar}")

# Delete other .tar.gz files except the selected repro
for f in tar_files:
    if f != target_repro_tar:
        file_path = os.path.join(group_path, f)
        os.remove(file_path)
        print(f"Deleted old archive: {f}")

# Extract the selected repro tar.gz
target_tar_path = os.path.join(group_path, target_repro_tar)
extract_dir = group_path  # Extract into the group_path
print(f"Extracting {target_tar_path}...")
with tarfile.open(target_tar_path, 'r:gz') as tar:
    tar.extractall(path=extract_dir)
print("Extraction completed.")

# Step 4: Only keep 'reproduce.sh' and 'README.md' inside the submission folder
submission_dir = os.path.join(group_path, os.path.splitext(os.path.splitext(target_repro_tar)[0])[0], 'submission')
print(f"Cleaning submission directory: {submission_dir}")

# Files to keep
keep_files = {'reproduce.sh', 'README.md'}

# Walk through the submission directory and remove unwanted files
for root, dirs, files in os.walk(submission_dir):
    for file in files:
        if file not in keep_files:
            delete_path = os.path.join(root, file)
            os.remove(delete_path)
            print(f"Deleted file: {delete_path}")

print("All tasks completed successfully!")