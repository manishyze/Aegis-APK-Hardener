#!/usr/bin/env bash

GREEN="\033[1;32m"
YELLOW="\033[1;33m"
CYAN="\033[1;36m"
RED="\033[1;31m"
RESET="\033[0m"

echo -e "${CYAN}[*] Initializing Aegis-APK-Hardener Environment Setup...${RESET}"

if command -v pkg &> /dev/null; then
    echo -e "${YELLOW}[*] Termux environment detected. Installing all required dependencies...${RESET}"
    pkg update -y && pkg upgrade -y
    pkg install -y python clang cmake make openjdk-17 zipalign apksigner apktool git
elif command -v apt &> /dev/null; then
    echo -e "${YELLOW}[*] Linux environment detected. Installing dependencies...${RESET}"
    sudo apt update -y
    sudo apt install -y python3 python3-pip build-essential cmake default-jdk zipalign apksigner apktool git
fi

# Set executable permissions for all modules
chmod +x cli/aegis_cli.py
chmod +x cli/ai_auditor.py
chmod +x cli/apk_processor.py
chmod +x cli/apk_injector.py
chmod +x setup.sh

echo -e "\n${GREEN}[✓] All core security tools (including apktool & Java) installed successfully!${RESET}\n"
sleep 1

python3 cli/aegis_cli.py
