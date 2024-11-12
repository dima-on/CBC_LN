import requests
from Info import config
import os


class Connect:
    """Class for controll of client"""

    def __init__(self, ip: str, comands_names: dict[str, str]) -> None:
        self.Ip: str = ip
        self.comands_names: dict[str, str] = comands_names

    def Add_File(self, file_path: str, current_path: str) -> tuple[any, int]:
        """Add file from client to server"""

        url = self.Ip + "/" + self.comands_names["Add File"]
        with open(config.CLIENT_DIRECTORY + current_path + file_path, "rb") as file:
            file_name: str = file_path

            files = {"file": (file)}

            data_dict = {"name": file_name, "current path": current_path}
            response = requests.post(url=url, files=files, data=data_dict)

            file_size = os.path.getsize(
                config.CLIENT_DIRECTORY + current_path + "\\" + file_path
            )

            return response, file_size

    def Remove_File(self, file_name: str, current_path: str) -> requests:
        """
        Remove file from Server \n
        Call from client to server
        """

        url = self.Ip + "/" + self.comands_names["Remove File"]

        data_dict = {"name": file_name, "current_path": current_path}

        response = requests.post(url=url, data=data_dict)

        return response

    def Check_Removed(self, file_names: list[str], current_path: str) -> list[str]:
        """
        Check removed file \n
        call from clien to server
        """

        url = self.Ip + "/" + self.comands_names["Check Removed"]
        data_dict = {
            "names": str(file_names),
            "current_path": current_path,
        }

        response = requests.get(url=url, data=data_dict)
        return eval(response.text)

    def Add_Folder(self, folder_path: str) -> requests:
        url = self.Ip + "/" + self.comands_names["Add Folder"]
        data_dict = {"name": folder_path}

        response = requests.post(url=url, data=data_dict)

    def Change_File(self, file_path: str, current_path: str) -> requests:
        """
        Change file on the server \n
        call from client to server
        """
        url = self.Ip + "/" + self.comands_names["Change File"]
        with open(config.CLIENT_DIRECTORY + current_path + file_path, "rb") as file:
            file_name: str = file_path

            files = {"file": (file)}

            data_dict = {"name": file_name, "current path": current_path}

            response = requests.post(url=url, files=files, data=data_dict)
            return response.text

    def Check_File(self, file_path: str, current_path) -> requests:
        """
        Check file was changed \n
        call from client to server
        """

        url = self.Ip + "/" + self.comands_names["Check File"]
        with open(config.CLIENT_DIRECTORY + current_path + file_path, "rb") as file:
            file_name: str = file_path

            files = {"file": (file)}  # str
            data_dict = {"name": file_name, "current path": current_path}

            response = requests.get(url=url, files=files, data=data_dict)
            return response

    def Get_Status(self) -> requests:
        """
        Get info \n
        call from client to server
        """
        url = self.Ip + "/" + self.comands_names["Get Status"]
        respounse = requests.get(url=url)
        return respounse
