#!/usr/bin/env python3
import sys
import os
import argparse
from ai_auditor import AIAuditor
from apk_processor import APKProcessor
from apk_injector import APKInjector

RED     = "\033[1;31m"
GREEN   = "\033[1;32m"
YELLOW  = "\033[1;33m"
BLUE    = "\033[1;34m"
CYAN    = "\033[1;36m"
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
    parser.add_argument("-i", "--apk", help="Path to input APK")
    parser.add_argument("-o", "--output", default="hardened_app.apk", help="Path for protected output APK")
    parser.add_argument("--audit", action="store_true", help="Run vulnerability audit")
    parser.add_argument("--shield", action="store_true", help="Inject C++ RASP Protection & DEX Shield")
    
    args = parser.parse_args()

    if not args.apk:
        print(f"{YELLOW}Usage: python3 cli/aegis_cli.py -i <APK_PATH> --audit --shield -o hardened.apk{RESET}\n")
        sys.exit(1)

    target_path = args.apk
    if not os.path.exists(target_path):
        print(f"{RED}[!] Error: Target {target_path} not found!{RESET}")
        sys.exit(1)

    if args.audit:
        print(f"{GREEN}[+] Initializing Security & Vulnerability Auditor...{RESET}")
        auditor = AIAuditor(target_path)
        auditor.audit_manifest(target_path)
        auditor.generate_report()

    if args.shield:
        print(f"{BLUE}[*] Initializing Aegis Native Hardening Engine...{RESET}")
        
        # 1. Inject Code
        injector = APKInjector(target_path)
        if injector.decompile():
            injector.inject_payload()
            recompiled = injector.recompile()
            
            # 2. Align & Sign
            if recompiled:
                processor = APKProcessor(recompiled, args.output)
                processor.align_and_sign()
                # Clean up intermediate file
                if os.path.exists(recompiled):
                    os.remove(recompiled)

if __name__ == "__main__":
    main()
