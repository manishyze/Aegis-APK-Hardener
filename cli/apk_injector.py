#!/usr/bin/env python3
import os
import subprocess
import shutil

CYAN    = "\033[1;36m"
GREEN   = "\033[1;32m"
YELLOW  = "\033[1;33m"
RED     = "\033[1;31m"
RESET   = "\033[0m"

class APKInjector:
    def __init__(self, target_apk):
        self.target_apk = target_apk
        self.decompiled_dir = target_apk.replace(".apk", "_decompiled")
        self.recompiled_apk = target_apk.replace(".apk", "_recompiled.apk")

    def decompile(self):
        print(f"{CYAN}[*] Decompiling target APK using Apktool...{RESET}")
        
        apktool_bin = shutil.which("apktool") or "/data/data/com.termux/files/usr/bin/apktool"
        
        cmd = [apktool_bin, "d", "-f", self.target_apk, "-o", self.decompiled_dir]
        res = subprocess.run(cmd, capture_output=True, text=True)
        
        if res.returncode != 0:
            print(f"{RED}[!] Decompilation failed! Error Output below:{RESET}")
            print(f"{YELLOW}{res.stderr}{RESET}")
            return False
        return True

    def inject_payload(self):
        print(f"{CYAN}[*] Injecting Aegis C++ Shield & Smali Hooks...{RESET}")
        
        smali_dir = os.path.join(self.decompiled_dir, "smali", "com", "aegis", "hardener")
        os.makedirs(smali_dir, exist_ok=True)
        
        smali_content = """
.class public Lcom/aegis/hardener/AegisNative;
.super Ljava/lang/Object;
.method public static native initSecurityChecks()Z
.end method
"""
        with open(os.path.join(smali_dir, "AegisNative.smali"), "w") as f:
            f.write(smali_content.strip())
            
        lib_dir = os.path.join(self.decompiled_dir, "lib", "arm64-v8a")
        os.makedirs(lib_dir, exist_ok=True)
        
        with open(os.path.join(lib_dir, "libaegis.so"), "w") as f:
            f.write("DUMMY_BINARY_DATA_FOR_NOW")
            
        print(f"{GREEN}[✓] Native Shield modules injected into APK structure.{RESET}")
        return True

    def recompile(self):
        print(f"{CYAN}[*] Recompiling APK...{RESET}")
        apktool_bin = shutil.which("apktool") or "/data/data/com.termux/files/usr/bin/apktool"
        aapt_bin = shutil.which("aapt") or "/data/data/com.termux/files/usr/bin/aapt"
        
        # 1. Primary build attempt (AAPT2)
        cmd = [apktool_bin, "b", self.decompiled_dir, "-o", self.recompiled_apk]
        res = subprocess.run(cmd, capture_output=True, text=True)
        
        # 2. Fallback using legacy AAPT (-a flag) if AAPT2 strict validation fails
        if res.returncode != 0 and os.path.exists(aapt_bin):
            print(f"{YELLOW}[!] AAPT2 build failed. Retrying recompilation with legacy AAPT (-a {aapt_bin})...{RESET}")
            cmd_fallback = [apktool_bin, "b", "-a", aapt_bin, self.decompiled_dir, "-o", self.recompiled_apk]
            res = subprocess.run(cmd_fallback, capture_output=True, text=True)

        if os.path.exists(self.decompiled_dir):
            shutil.rmtree(self.decompiled_dir)
            
        if res.returncode == 0 and os.path.exists(self.recompiled_apk):
            print(f"{GREEN}[✓] APK Recompiled Successfully: {self.recompiled_apk}{RESET}")
            return self.recompiled_apk
        else:
            print(f"{RED}[!] Recompilation failed. Error Output below:{RESET}")
            print(f"{YELLOW}{res.stderr}{RESET}")
            return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        injector = APKInjector(sys.argv[1])
        if injector.decompile():
            injector.inject_payload()
            injector.recompile()
