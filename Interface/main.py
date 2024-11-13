from Backend import connect, server, synchronization
from Info import config
import threading
import os
from functools import lru_cache
import math

class Client:
    def __init__(self, func) -> None:
        self.Client_Class = connect.Connect(config.IP, comands_names=config.PATH_NAME)
        self.Data: dict = {
            "Add elements": [],
            "Remove elements": [],
            "Change elements": [],
        }
        self.Size = 0
        self.Current_Size = 0
        self.func = func

    def Get_Full_Size(self, current_path: str = "") -> int:
        for element in os.listdir(config.CLIENT_DIRECTORY + current_path):
            # Check folder
            if os.path.isdir(config.CLIENT_DIRECTORY + current_path + element):
                self.Get_Full_Size(current_path + element + "\\\\")
                continue
            # File is be

            is_be = self.Client_Class.Check_File(element, current_path, 0).text
            if is_be == "False":
                size = os.path.getsize(config.CLIENT_DIRECTORY + current_path + "\\\\" + element)

                size /= 1000000000

                self.Size += size
                print(element, size)
        
        return self.Size

    def syn(self, current_path: str = "") -> list:
        """This func synchronizate client and server"""

        for element in os.listdir(config.CLIENT_DIRECTORY + current_path):
            # Check folder
            if os.path.isdir(config.CLIENT_DIRECTORY + current_path + element):
                self.Client_Class.Add_Folder(current_path + element)
                self.syn(current_path + element + "\\\\")
                continue
            # File is be

            res, _ = self.Client_Class.Add_File(element, current_path)
            if res.status_code == 200:
                wei = os.path.getsize(config.CLIENT_DIRECTORY + current_path + "\\" + element)
                self.Data["Add elements"] = list(self.Data["Add elements"]) + [
                    [element, wei]
                ]
                self.Current_Size -= (wei / 1000000000)
                proc = round((1 - (self.Current_Size / self.Size)) * 100, 2)

                self.func[0](proc)
                self.func[1](element, wei)
                
                print(element, str(proc) + "%")
                continue
            response = self.Client_Class.Check_File(element, current_path, 1)
            if response.text == "True":

                self.Client_Class.Change_File(element, current_path)
                path = config.CLIENT_DIRECTORY + current_path + element
                size = os.path.getsize(path)
                self.Data["Change elements"] = list(self.Data["Change elements"]) + [
                    [element, size]
                ]

        # was File remover
        removed_names: list[str] = self.Client_Class.Check_Removed(
            os.listdir(config.CLIENT_DIRECTORY + current_path), current_path
        )
        for removed_name in removed_names:
            # Remove file
            res = self.Client_Class.Remove_File(removed_name, current_path)
            try:
                size = int(res.text)
            except ValueError as e:
                size = 0
            self.Data["Remove elements"] = list(self.Data["Remove elements"]) + [
                [removed_name, size]
            ]


class Server:
    def __init__(self) -> None:
        self.Server_Class = server.Server(config.PORT)

    def Get_Info(self):
        return self.Server_Class.Get_Info()

    def Run(self):
        self.Server_Class.Start_Server()
