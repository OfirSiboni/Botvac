import logging as log
import os
import subprocess
import winreg

import schedule


class Watchdog:
    INTERVAL = int(os.getenv("MVP_INTERVAL", 30))

    def __init__(self, interval: int = None):
        registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)
        self.EXE_PATH = str(winreg.QueryValueEx(key, "MVP")[0])
        self.interval = interval or self.interval

        log.info("Created watchdog")
        log.warning(f"EXE_PATH = {self.EXE_PATH}")

    def _check_running(self, name):
        return name in str(subprocess.check_output('tasklist', shell=True))

    def _wakeup_routine(self):
        if not self._check_running('MVP.exe'):
            subprocess.Popen([self.EXE_PATH],
                             shell=False, close_fds=True,
                             creationflags=subprocess.DETACHED_PROCESS)

    def main(self):
        schedule.every(self.interval).seconds.do(self._wakeup_routine)
        while True:
            schedule.run_pending()


if __name__ == "__main__":
    watch = Watchdog()
    watch.main()
