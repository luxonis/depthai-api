#!/usr/bin/env python3
import sys
import os
import subprocess
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('-sdai', "--skip_depthai", action="store_true", help="Skip installation of depthai library.")
args = parser.parse_args()

# 3rdparty dependencies to install
DEPENDENCIES = ['opencv-python', 'pyyaml', 'requests', 'blobconverter']

# Constants
ARTIFACTORY_URL = 'https://artifacts.luxonis.com/artifactory/luxonis-python-snapshot-local'

# Check if in virtual environment
in_venv = getattr(sys, "real_prefix", getattr(sys, "base_prefix", sys.prefix)) != sys.prefix
pip_call = [sys.executable, "-m", "pip"]
pip_install = pip_call + ["install"]
if not in_venv:
    pip_install.append("--user")

# Update pip
subprocess.check_call([*pip_install, "pip", "-U"])
# Install opencv-python
subprocess.check_call([*pip_install, *DEPENDENCIES])

if not args.skip_depthai:
    # Check if in git context and retrieve some information
    git_context = False
    git_commit = ""
    git_branch = ""
    try:
        git_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('UTF-8').strip()
        git_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('UTF-8').strip()
        git_context = True
    except (OSError, subprocess.CalledProcessError) as e: 
        pass  # we're not in a git context

    # Install depthai depending on context
    if not git_context or git_branch == 'main':
        # Install latest pypi depthai release
        subprocess.check_call([*pip_install, '-U', '--force-reinstall', 'depthai'])
    elif git_context:
        try:
            subprocess.check_output(['git', 'submodule', 'update', '--init', '--recursive'])
        except (OSError, subprocess.CalledProcessError) as e: 
            print("git submodule update failed!")
            raise
        with Path(__file__).resolve().parent.parent as repo_root:
            sys.path.append(str(repo_root.absolute()))
            import find_version
            # Get package version if in git context
            final_version = find_version.get_package_dev_version(git_commit)
            # Install latest built wheels from artifactory (0.0.0.0+[hash] or [version]+[hash])
            commands = [[*pip_install, "--extra-index-url", ARTIFACTORY_URL, "depthai=="+final_version],
                        [*pip_install, "."]]
            success = False
            for command in commands:
                try:
                    success = subprocess.call(command) == 0
                except (OSError, subprocess.CalledProcessError) as e:
                    success = False
                if success:
                    break
            # If all commands failed
            if not success:
                print("Couldn't install dependencies as wheels and trying to compile from sources failed")
                print("Check https://github.com/luxonis/depthai-python#dependencies on retrieving dependencies for compiling from sources")

resources = {
    "models/tiny-yolo-v3.yml": "https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/tiny-yolo-v3.yml",
    "dataset.zip": "https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/dataset.zip",
    "construction_vest.mp4": "https://artifacts.luxonis.com/artifactory/luxonis-depthai-data-local/network/construction_vest.mp4"
}
import requests
import zipfile

for path, url in resources.items():
    print(f"Downloading {path}")
    r = requests.get(url)
    r.raise_for_status()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'wb') as f:
        f.write(r.content)

    if Path(path).suffix == '.zip':
        with zipfile.ZipFile(path) as zip_f:
            zip_f.extractall(".")
