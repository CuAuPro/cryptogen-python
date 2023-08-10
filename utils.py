import os
import platform

def find_keytool_executable():
    system_platform = platform.system()
    if system_platform == "Windows":
        executable_name = "keytool.exe"
    else:
        executable_name = "keytool"

    for path in os.environ["PATH"].split(os.pathsep):
        executable_path = os.path.join(path, executable_name)
        if os.access(executable_path, os.X_OK):
            return executable_path
    return None