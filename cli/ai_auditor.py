#!/usr/bin/env python3
import os
import re
import json

RED     = "\033[1;31m"
GREEN   = "\033[1;32m"
YELLOW  = "\033[1;33m"
CYAN    = "\033[1;36m"
BOLD    = "\033[1m"
RESET   = "\033[0m"

class AIAuditor:
    def __init__(self, target_dir):
        self.target_dir = target_dir
        self.findings = []

    def audit_manifest(self, manifest_path):
        """Scans AndroidManifest.xml for insecure configurations."""
        if not os.path.exists(manifest_path):
            return

        print(f"{CYAN}[*] Auditing AndroidManifest.xml...{RESET}")
        with open(manifest_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Check debuggable flag
        if 'android:debuggable="true"' in content:
            self.findings.append({
                "severity": "HIGH",
                "title": "Application is Debuggable",
                "desc": "android:debuggable='true' allows attacker debugging via ADB.",
                "patch": "Set android:debuggable='false' in AndroidManifest.xml."
            })

        # Check allowBackup flag
        if 'android:allowBackup="true"' in content:
            self.findings.append({
                "severity": "MEDIUM",
                "title": "Application Backup Allowed",
                "desc": "android:allowBackup='true' allows ADB data extraction without root.",
                "patch": "Set android:allowBackup='false'."
            })

        # Check cleartext traffic permission
        if 'android:usesCleartextTraffic="true"' in content:
            self.findings.append({
                "severity": "HIGH",
                "title": "Cleartext HTTP Traffic Allowed",
                "desc": "App permits unencrypted HTTP traffic susceptible to MITM.",
                "patch": "Set android:usesCleartextTraffic='false' and enforce HTTPS."
            })

    def audit_code_secrets(self):
        """Scans source/smali files for hardcoded sensitive strings."""
        print(f"{CYAN}[*] Scanning decompiled code for hardcoded secrets & weak cryptography...{RESET}")
        
        # Regex patterns for secret detection
        patterns = {
            "Hardcoded API Key": r'(?i)(api[_-]?key|secret|token)\s*=\s*["\'][A-Za-z0-9_\-]{16,}["\']',
            "Hardcoded Private Key": r'-----BEGIN (RSA|EC|PRIVATE) KEY-----',
            "Weak Cryptography (DES/MD5)": r'(?i)(Cipher\.getInstance\("DES"\)|MessageDigest\.getInstance\("MD5"\))'
        }

        for root, _, files in os.walk(self.target_dir):
            for file in files:
                if file.endswith((".java", ".smali", ".xml", ".json")):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            for rule_name, pattern in patterns.items():
                                if re.search(pattern, content):
                                    self.findings.append({
                                        "severity": "HIGH",
                                        "title": f"Security Risk: {rule_name}",
                                        "desc": f"Sensitive pattern detected in file: {os.path.basename(file_path)}",
                                        "patch": "Obfuscate sensitive strings or load securely via encrypted C++ Native Layer."
                                    })
                    except Exception:
                        pass

    def generate_report(self):
        """Prints formatted vulnerability report."""
        print(f"\n{BOLD}{YELLOW}====================================================================={RESET}")
        print(f"{BOLD}{YELLOW}                    🛡️ AEGIS SECURITY AUDIT REPORT                  {RESET}")
        print(f"{BOLD}{YELLOW}====================================================================={RESET}\n")

        if not self.findings:
            print(f"{GREEN}[✓] No high-risk static vulnerabilities detected.{RESET}\n")
            return

        for idx, item in enumerate(self.findings, 1):
            color = RED if item['severity'] == 'HIGH' else YELLOW
            print(f"{color}[Finding #{idx}] [{item['severity']}] {item['title']}{RESET}")
            print(f"  • Description : {item['desc']}")
            print(f"  • Auto-Patch  : {item['patch']}\n")

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    auditor = AIAuditor(target)
    auditor.audit_manifest(os.path.join(target, "AndroidManifest.xml"))
    auditor.audit_code_secrets()
    auditor.generate_report()
