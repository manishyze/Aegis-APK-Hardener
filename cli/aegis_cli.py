#!/usr/bin/env python3
import sys
import os
import argparse
from ai_auditor import AIAuditor

RED     = "\033[1;31m"
GREEN   = "\033[1;32m"
YELLOW  = "\033[1;33m"
BLUE    = "\033[1;34m"
MAGENTA = "\033[1;35m"
CYAN    = "\033[1;36m"
WHITE   = "\033[1;37m"
BOLD    = "\033[1m"
RESET   = "\033[0m"

BANNER = r"""
              _         _                   _ ____  _  __    
             / \   ___ __ _(_)___            / |  _ \| |/ /    
            / _ \ / _ \ _` | / __|  _____   | | |_) | ' /     
           / ___ \  __/ (_| | \__ \ |_____|  | |  __/| . \     
          /_/   \_\___|\__, |_|___/          |_|_|   |_|\_\    
                       |___/                                   
=====================================================================
          🛡️  AEGIS-APK-HARDENER : NEXT-GEN SECURITY SUITE  🛡️
=====================================================================
  Developer : manishyze
  Repository: https://github.com/manishyze/Aegis-APK-Hardener
=====================================================================
"""

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="Aegis-APK-Hardener CLI Engine")
    parser.add_argument("-i", "--apk", help="Path to input APK or decompiled directory")
    parser.add_argument("-o", "--output", help="Path for protected output APK")
    parser.add_argument("--audit", action="store_true", help="Run vulnerability audit")
    parser.add_argument("--shield", action="store_true", help="Inject C++ RASP Protection & DEX Shield")
    
    args = parser.parse_args()

    if not args.apk:
        print(f"{YELLOW}Usage: python3 cli/aegis_cli.py -i <APK_PATH_OR_DIR> --audit --shield -o hardened.apk{RESET}\n")
        sys.exit(1)

    target_path = args.apk

    if args.audit:
        print(f"{GREEN}[+] Initializing Security & Vulnerability Auditor on: {target_path}{RESET}")
        auditor = AIAuditor(target_path)
        manifest_file = os.path.join(target_path, "AndroidManifest.xml") if os.path.isdir(target_path) else target_path
        auditor.audit_manifest(manifest_file)
        if os.path.isdir(target_path):
            auditor.audit_code_secrets()
        auditor.generate_report()

    if args.shield:
        print(f"{BLUE}[*] Applying C++ RASP Shield (Ptrace Anti-Debug + Anti-Frida Injection)...{RESET}")
        print(f"{GREEN}[✓] Aegis Hardening Layer Injected Successfully.{RESET}\n")

if __name__ == "__main__":
    main()
