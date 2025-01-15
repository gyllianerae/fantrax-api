#!/usr/bin/env bash
set -e  # Exit immediately if a command exits with a non-zero status

# Update packages and install dependencies
apt-get update
apt-get install -y wget unzip

# Install Google Chrome
wget -qO- https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O google-chrome.deb
dpkg -i google-chrome.deb || apt-get install -y --fix-broken  # Force fix missing dependencies

# Clean up
rm google-chrome.deb

# Confirm installation path
echo "Google Chrome installed at: $(which google-chrome)"
