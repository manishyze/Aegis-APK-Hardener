#include <jni.h>
#include <string>
#include <unistd.h>
#include <sys/ptrace.h>
#include <fstream>
#include <android/log.h>

#define LOG_TAG "AegisNative"
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR, LOG_TAG, __VA_ARGS__)

// 1. Anti-Debugging Check using ptrace
bool check_ptrace_attach() {
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) < 0) {
        LOGE("[CRITICAL] Debugger detected via ptrace! Terminating application.");
        return true; // Debugger attached
    }
    return false;
}

// 2. Anti-Frida & Anti-Xposed Runtime Scan (/proc/self/maps)
bool check_frida_injection() {
    std::ifstream maps("/proc/self/maps");
    std::string line;
    while (std::getline(maps, line)) {
        if (line.find("frida") != std::string::npos || 
            line.find("xposed") != std::string::npos || 
            line.find("gadget") != std::string::npos) {
            LOGE("[CRITICAL] Memory Hooking Framework (Frida/Xposed) detected in process memory!");
            return true; // Frida or Xposed detected
        }
    }
    return false;
}

extern "C" JNIEXPORT jboolean JNICALL
Java_com_aegis_hardener_AegisNative_initSecurityChecks(JNIEnv* env, jobject thiz) {
    LOGI("Aegis Native Security Engine Initialized.");

    if (check_ptrace_attach()) {
        return JNI_FALSE; // Security breach
    }

    if (check_frida_injection()) {
        return JNI_FALSE; // Security breach
    }

    return JNI_TRUE; // System Secure
}
