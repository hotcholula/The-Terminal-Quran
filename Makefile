# Programmed by Aryan Chandavarkar
VENV_DIR := venv

.PHONY: all install install-venv

all: install

install: install-venv
	@echo "Copying files..."
	@sudo mkdir -p /usr/local/The-Terminal-Quran
	@sudo cp -r * /usr/local/The-Terminal-Quran
	@sudo ln -sf /usr/local/The-Terminal-Quran/quran.py /usr/local/bin/quran
	@sudo chmod +x /usr/local/The-Terminal-Quran/quran.py
	@sudo chmod +x /usr/local/bin/quran
	@echo "In the Name of Allah The Most Gracious the Most Merciful. Salutations be upon God's Final Prophet, Muhammad. As Salamu Alaykum [Peace be upon you]. I, Aryan Muhammad Chandavarkar, pray this Holy Qur'an brings you and me goodness, guidance, and forgiveness of sin. May He enter us into the Gardens of Paradise and protect us from the Fires of Hell. May He make this a source of good deeds for me and you until the Day of Judgement. Ameen."

install-venv:
	@echo "Creating virtual environment..."
	@python3 -m venv $(VENV_DIR)
	@echo "Installing dependencies in virtual environment..."
	@$(VENV_DIR)/bin/pip install termcolor tabulate
	@echo "Virtual environment and dependencies installed."

clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV_DIR)
	@echo "Cleaned."
