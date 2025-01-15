#!/usr/bin/env bash
set -e  # Exit immediately if a command exits with a non-zero status

# Update packages and install dependencies
apt-get update
apt-get install -y wget unzip

# Install Google Chrome stable version
wget -qO- https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O google-chrome.deb
apt-get install -y ./google-chrome.deb || apt --fix-broken install -y

# Clean up
rm google-chrome.deb

echo "Google Chrome installed!"
