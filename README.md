In the Name of Allah, the Most Gracious, the Most Merciful
# The Terminal Quran
Programmed by: Aryan Chandavarkar

A command-line application to read and parse the Quran.

## Requirements

- Python 3
- `termcolor` library
- `tabulate` library

### Install Requirements

#### Ubuntu and Debian-based Distros

1. Install Python 3 and pip:
    ```sh
    sudo apt update
    sudo apt install python3 python3-pip
    ```

#### Arch-based Distros

1. Install Python 3 and pip:
    ```sh
    sudo pacman -S python python-pip
    ```

#### macOS

1. Install Homebrew if not already installed:
    ```sh
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

## Installation

### Using the Makefile

#### All Platforms

1. Open a terminal and run the following commands:

    ```sh
    # Clone the GitHub repository
    git clone https://github.com/hotcholula/The-Terminal-Quran.git

    # Navigate to the project directory
    cd The-Terminal-Quran

    # Run the Makefile to install
    make install
    ```

### Manual Installation

1. Download the repository from GitHub:
   - Click on the green "Code" button and select "Download ZIP".
   - Extract the ZIP file to a directory of your choice.

2. Open a terminal and navigate to the directory where you extracted the files.

3. Install dependencies and set up the project:
    ```sh
    pip3 install termcolor tabulate
    sudo mkdir -p /usr/local/The-Terminal-Quran
    sudo cp -r * /usr/local/The-Terminal-Quran
    sudo ln -sf /usr/local/The-Terminal-Quran/quran.py /usr/local/bin/quran
    sudo chmod +x /usr/local/The-Terminal-Quran/quran.py
    sudo chmod +x /usr/local/bin/quran
    ```

## Usage

After installing, you can use the `quran` command followed by the desired options:

```sh
quran <command> [<args>] [-a | -e] [-nc] [-nh]
