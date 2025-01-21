#!/bin/bash

# Exit on any error
set -e
pip install -r .github/downloader/requirements.txt
cd .github/downloader/ && npm install && cd ../..

python .github/downloader/ci_daily_update.py
python .github/scripts/workspace/organize_files.py
