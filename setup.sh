#!/usr/bin/env bash

# Colors
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
CYAN="\033[1;36m"
RED="\033[1;31m"
RESET="\033[0m"

echo -e "${CYAN}[*] Initializing Aegis-APK-Hardener Environment Setup...${RESET}"

# Detect Package Manager (Termux pkg or Linux apt)
if command -v pkg &> /dev/null; then
    echo -e "${YELLOW}[*] Termux environment detected. Updating packages...${RESET}"
    pkg update -y && pkg upgrade -y
    echo -e "${YELLOW}[*] Installing dependencies (python, clang, cmake, openjdk-17, zipalign)...${RESET}"
    pkg install -y python clang cmake make openjdk-17 zipalign apksigner git
elif command -v apt &> /dev/null; then
    echo -e "${YELLOW}[*] Debian/Ubuntu environment detected. Updating packages...${RESET}"
    sudo apt update -y
    echo -e "${YELLOW}[*] Installing dependencies...${RESET}"
    sudo apt install -y python3 python3-pip build-essential cmake default-jdk zipalign apksigner git
else
    echo -e "${RED}[!] Unknown package manager. Please install dependencies manually.${RESET}"
fi

# Set executable permissions
chmod +x cli/aegis_cli.py
chmod +x setup.sh

echo -e "\n${GREEN}[✓] All core security dependencies and tools installed successfully!${RESET}\n"
sleep 1

# Launch Aegis CLI Banner & Feature Overview
python3 cli/aegis_cli.py
