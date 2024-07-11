#!/bin/bash

# Define the installation directory
INSTALL_DIR="/usr/local/The-Terminal-Quran"
BIN_DIR="/usr/local/bin"

# Create the installation directory
sudo mkdir -p $INSTALL_DIR
sudo mkdir -p $BIN_DIR

# Copy the files to the installation directory
sudo cp -r * $INSTALL_DIR

# Create a symbolic link to the script in /usr/local/bin
sudo ln -sf $INSTALL_DIR/quran.py $BIN_DIR/quran

# Make the script executable
sudo chmod +x $INSTALL_DIR/quran.py
sudo chmod +x $BIN_DIR/quran

echo "Quran CLI installed successfully. You can now run 'quran' from anywhere in your terminal."

