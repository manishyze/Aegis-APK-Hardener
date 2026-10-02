#!/usr/bin/env python3
import sys
import time

# ANSI Color Codes for Terminal
RED     = "\033[1;31m"
GREEN   = "\033[1;32m"
YELLOW  = "\033[1;33m"
BLUE    = "\033[1;34m"
MAGENTA = "\033[1;35m"
CYAN    = "\033[1;36m"
WHITE   = "\033[1;37m"
BOLD    = "\033[1m"
RESET   = "\033[0m"

BANNER = f"""{RED}{BOLD}
              _         _                   _ ____  _  __    
             / \   ___ __ _(_)___            / |  _ \| |/ /    
            / _ \ / _ \ _` | / __|  _____   | | |_) | ' /     
           / ___ \  __/ (_| | \__ \ |_____|  | |  __/| . \     
          /_/   \_\___|\__, |_|___/          |_|_|   |_|\_\    
                       |___/                                   
{CYAN}====================================================================={RESET}
{YELLOW}{BOLD}          🛡️  AEGIS-APK-HARDENER : NEXT-GEN SECURITY SUITE  🛡️{RESET}
{CYAN}====================================================================={RESET}
{MAGENTA}{BOLD}  Developer : manishyze{RESET}
{BLUE}  Repository: https://github.com/manishyze/Aegis-APK-Hardener{RESET}
{CYAN}====================================================================={RESET}
"""

FEATURES = f"""
{WHITE}{BOLD}[ Core Features & Security Modules ]{RESET}

{GREEN}  [✓] 1. Native C++ Code Obfuscation & Protection{RESET}
      • DEX-to-Native Encryption (.so wrapper)
      • Anti-Decompilation Headers (Crashes JADX / APKTool)
      • Dynamic AES-256 String & Asset Obfuscation

{GREEN}  [✓] 2. Runtime Application Self-Protection (RASP){RESET}
      • Anti-Frida & Anti-Xposed Memory Injection Detection
      • Anti-Debugging Engine (Native ptrace Guard against IDA/GDB)
      • Memory Dump Protection (Blocks GameGuardian / Cheat Engine)

{GREEN}  [✓] 3. Environment & Integrity Verification{RESET}
      • SHA-256 Signature Lock (Auto-detects APK tampering)
      • Kernel-level Anti-Root (Magisk, KernelSU, Zygisk)
      • Anti-Emulator Lockdown (Blocks BlueStacks, Nox, Virtual Clones)

{GREEN}  [✓] 4. Autonomous AI Code Auditor & Auto-Patcher{RESET}
      • Automatic Code Vulnerability & Memory Leak Scanning
      • Zero-Source-Code Modification Engine (One-Command Shielding)
"""

def main():
    print(BANNER)
    print(FEATURES)
    print(f"{CYAN}====================================================================={RESET}")
    print(f"{YELLOW}{BOLD}  [ System Ready ] Run 'python3 cli/aegis_cli.py --help' to start.{RESET}")
    print(f"{CYAN}====================================================================={RESET}\n")

if __name__ == "__main__":
    main()
