package com.aegis.hardener;

public class AegisNative {
    static {
        // Load compiled C++ shared library
        System.loadLibrary("aegis");
    }

    // Native C++ Security Methods
    public native boolean initSecurityChecks();

    public static void verifyEnvironment() {
        AegisNative aegis = new AegisNative();
        boolean isSecure = aegis.initSecurityChecks();
        
        if (!isSecure) {
            // Self-terminate if debugger, Frida or tampering is detected
            System.exit(1);
        }
    }
}
