#!/usr/bin/env bash
set -e  # Exit immediately if a command exits with a non-zero status

# Update packages
apt-get update

# Install dependencies
apt-get install -y wget apt-transport-https ca-certificates gnupg

# Add Google Chrome official key and repository
wget -qO - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg
echo "deb [signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list

# Install Google Chrome
apt-get update
apt-get install -y google-chrome-stable

# Print the installed Chrome version and location
google-chrome --version
which google-chrome
