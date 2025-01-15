#!/usr/bin/env bash
set -e  # Exit immediately if a command exits with a non-zero status

# Update packages and install dependencies
apt-get update
apt-get install -y wget unzip
apt-get install -y chromium-browser
apt-get install -y libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2
apt-get install -y fonts-liberation xdg-utils libappindicator3-1
apt-get install -y libx11-xcb1 libxcb-dri3-0 libxcomposite1 libxrandr2
apt-get install -y libxi6 libxtst6 libxss1 libxkbcommon0 libgbm1

echo "Dependencies installed!"
