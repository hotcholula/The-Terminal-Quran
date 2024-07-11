In the Name of Allah, the Most Gracious, the Most Merciful

# The Terminal Quran

A command-line application to read and search the Quran.

## Installation

### Using the Installer Script

#### Ubuntu and Debian-based Distros

1. Open a terminal and run the following commands:

    ```sh
    # Update package list and install Git if not already installed
    sudo apt update
    sudo apt install git

    # Clone the GitHub repository
    git clone https://github.com/yourusername/The-Terminal-Quran.git

    # Navigate to the project directory
    cd The-Terminal-Quran

    # Run the installer script
    sudo ./install.sh
    ```

#### Arch-based Distros

1. Open a terminal and run the following commands:

    ```sh
    # Install Git if not already installed
    sudo pacman -S git

    # Clone the GitHub repository
    git clone https://github.com/yourusername/The-Terminal-Quran.git

    # Navigate to the project directory
    cd The-Terminal-Quran

    # Run the installer script
    sudo ./install.sh
    ```

#### macOS

1. Open a terminal and run the following commands:

    ```sh
    # Install Homebrew if not already installed
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Install Git if not already installed
    brew install git

    # Clone the GitHub repository
    git clone https://github.com/yourusername/The-Terminal-Quran.git

    # Navigate to the project directory
    cd The-Terminal-Quran

    # Run the installer script
    sudo ./install.sh
    ```

### Manual Installation

1. Download the repository from GitHub:
   - Click on the green "Code" button and select "Download ZIP".
   - Extract the ZIP file to a directory of your choice.

2. Open a terminal and navigate to the directory where you extracted the files.

3. Copy the files to `/usr/local/The-Terminal-Quran` and create a symbolic link:
   ```sh
   sudo mkdir -p /usr/local/The-Terminal-Quran
   sudo cp -r * /usr/local/The-Terminal-Quran
   sudo ln -sf /usr/local/The-Terminal-Quran/quran.py /usr/local/bin/quran
   sudo chmod +x /usr/local/The-Terminal-Quran/quran.py
   sudo chmod +x /usr/local/bin/quran

