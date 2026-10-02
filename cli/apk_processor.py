#!/usr/bin/env python3
import os
import subprocess
import shutil

RED     = "\033[1;31m"
GREEN   = "\033[1;32m"
YELLOW  = "\033[1;33m"
CYAN    = "\033[1;36m"
BOLD    = "\033[1m"
RESET   = "\033[0m"

class APKProcessor:
    def __init__(self, input_apk, output_apk="hardened_app.apk"):
        self.input_apk = input_apk
        self.output_apk = output_apk
        self.keystore_path = "aegis_debug.keystore"

    def generate_keystore(self):
        """Generates a default keystore for signing patched APKs."""
        if not os.path.exists(self.keystore_path):
            print(f"{CYAN}[*] Generating signing keystore ({self.keystore_path})...{RESET}")
            cmd = [
                "keytool", "-genkey", "-v",
                "-keystore", self.keystore_path,
                "-alias", "aegis_key",
                "-keyalg", "RSA",
                "-keysize", "2048",
                "-validity", "10000",
                "-storepass", "aegis123",
                "-keypass", "aegis123",
                "-dname", "CN=Aegis, OU=Hardener, O=Security, C=US"
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"{GREEN}[✓] Keystore generated successfully.{RESET}")

    def align_and_sign(self):
        """Aligns and signs the output APK."""
        self.generate_keystore()
        aligned_apk = "aligned_temp.apk"

        print(f"{CYAN}[*] Running ZipAlign optimization...{RESET}")
        zipalign_cmd = ["zipalign", "-f", "-p", "4", self.input_apk, aligned_apk]
        res = subprocess.run(zipalign_cmd, capture_output=True, text=True)

        target_for_sign = aligned_apk if res.returncode == 0 else self.input_apk

        print(f"{CYAN}[*] Signing APK using APKSigner...{RESET}")
        sign_cmd = [
            "apksigner", "sign",
            "--ks", self.keystore_path,
            "--ks-pass", "pass:aegis123",
            "--key-pass", "pass:aegis123",
            "--out", self.output_apk,
            target_for_sign
        ]
        sign_res = subprocess.run(sign_cmd, capture_output=True, text=True)

        if os.path.exists(aligned_apk):
            os.remove(aligned_apk)

        if sign_res.returncode == 0 and os.path.exists(self.output_apk):
            print(f"{GREEN}[✓] HARDENING COMPLETE! Output Saved: {self.output_apk}{RESET}\n")
            return True
        else:
            print(f"{RED}[!] APK Signing failed. Ensure apksigner is installed.{RESET}\n")
            return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        processor = APKProcessor(sys.argv[1])
        processor.align_and_sign()
