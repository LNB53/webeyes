#!/bin/bash

REPO_PATH="/var/www/webeyes"
BRANCH="main" # Replace with your branch name if different

cd $REPO_PATH || exit
unset GIT_DIR

# Pull the latest changes from the repository
git fetch origin $BRANCH
git reset --hard origin/$BRANCH

# Update submodules if any
git submodule update --init --recursive

# Optionally, you can add commands to restart services, clear caches, etc.
