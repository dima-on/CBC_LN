import os
import hashlib
import json
from datetime import datetime


class Checker:
    def __init__(self, path: str) -> None:
        self.Path = path

    def File_Is_Be(self, file_name: str) -> bool:
        """Is file be"""
        try:
            for element in os.listdir(self.Path):
                if element == file_name:
                    return True
        except:
            return False
        return False

    def Check_Changes(self, file_name: str, new_file: any) -> bool:
        """Check does new file have different bettwen old file"""
        try:
            with open(self.Path + file_name, "rb") as old_file:
                old_hash = self.Get_File_Hash(old_file)
                new_file.seek(0)
                new_hash = self.Get_File_Hash(new_file)

                return old_hash != new_hash
        except:
            return False

    def Get_File_Hash(self, file) -> str:
        """return hash"""

        hash_md5 = hashlib.md5()
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)

        return hash_md5.hexdigest()


class Data:
    def __init__(self, data_path: str) -> None:
        self.Data_Path = data_path

    def Write_Data(self, key: str, value: any) -> None:
        # """Write data in json file"""
        pass
        # with open(self.Data_Path, "r") as file:
        #     j_file = json.load(file)

        # j_file[key] = value

        # with open(self.Data_Path, "w") as file:
        #     json.dump(j_file, file)

    def Read_Data(self) -> dict:
        # """Read data from json file"""

        # with open(self.Data_Path, "r") as file:
        #     j_file = json.load(file)
        #     return dict(j_file)
        pass

    def Get_Normal_Time(self, time: float) -> str:
        """Get normal time"""
        return datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")
