import os
os.system('dir')


# import subprocess
# result = subprocess.run(['dir'])


print () 
print () 
import ctypes
kernel32 = ctypes.WinDLL('kernel32')
pid = kernel32.GetCurrentProcessId()
print(f"El ID del proceso actual es: {pid}")