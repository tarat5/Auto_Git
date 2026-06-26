import platform
import uuid

def get_device_info():
    os_name = f"{platform.system()} {platform.release()}"
    hardware_id = hex(uuid.getnode())

    return [os_name, hardware_id]


# Example
info = get_device_info()

print("OS:", info[0])
print("Hardware ID:", info[1])