# deviceid_android.py
import hashlib
import os
import uuid
import subprocess
import json

STORAGE_FILE = ".device_id.json"

def get_persistent_uuid():
    """Génère ou récupère un UUID persistant"""
    print(" ", end="")
    return

def get_android_id():
    """Récupère l'Android ID en utilisant des méthodes alternatives"""
    try:
        with open("/system/build.prop", "r") as f:
            for line in f:
                if line.startswith("ro.serialno="):
                    return line.strip().split("=")[1]
        
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line.startswith("Serial"):
                    return line.split(":")[1].strip()
    except:
        pass
    
    return get_persistent_uuid()

def get_hardware_id():
    mac = ""
    try:
        with open("/sys/class/net/wlan0/address", "r") as f:
            mac = f.read().strip()
    except:
        pass
    
    android_id = get_android_id()
    device_info = ""
    
    for file in ["/proc/cpuinfo", "/system/build.prop"]:
        try:
            with open(file, "r") as f:
                device_info += f.read()
        except:
            pass
    
    composite = f"{mac}-{android_id}-{device_info}"
    return hashlib.sha256(composite.encode()).hexdigest()

if __name__ == "__main__":
    device_id = get_hardware_id()
    print(f"""
    *************************************
    Votre ID Appareil : {device_id}
    *************************************
    Envoyez cet ID à l'administrateur pour activation
    """)