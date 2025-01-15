#!/usr/bin/env bash
set -e  # Exit if any command fails

# Install dependencies
apt-get update
apt-get install -y wget unzip

# Install Google Chrome
wget -qO- https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O google-chrome.deb
dpkg -i google-chrome.deb || apt-get install -y --fix-broken
rm google-chrome.deb

# Print Chrome binary location for verification
echo "Google Chrome binary path: $(which google-chrome)"
