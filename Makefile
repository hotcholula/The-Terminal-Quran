# Programmed by Aryan Chandavarkar
.PHONY: install dependencies

install: dependencies
	@echo "Installing The-Terminal-Quran..."
	sudo mkdir -p /usr/local/The-Terminal-Quran
	sudo cp -r * /usr/local/The-Terminal-Quran
	sudo ln -sf /usr/local/The-Terminal-Quran/quran.py /usr/local/bin/quran
	sudo chmod +x /usr/local/The-Terminal-Quran/quran.py
	sudo chmod +x /usr/local/bin/quran
	@echo "The Terminal Quran installed successfully. You can now run 'quran' from anywhere in your terminal. May your life be filled with guidance and goodness."

dependencies:
	@echo "Installing dependencies..."
	@if [ `uname` = "Darwin" ]; then \
		brew install python; \
	fi
	pip3 install termcolor tabulate
	@echo "Dependencies installed."

