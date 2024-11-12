from Backend import connect, server, synchronization
from Info import config
import threading
import os
from functools import lru_cache

class Client:
    def __init__(self) -> None:
        self.Client_Class = connect.Connect(config.IP, comands_names=config.PATH_NAME)
        self.Data :dict = {
            "Add elements": [],
            "Remove elements": [],
            "Change elements": []
        }
    def syn(self, current_path: str="", is_First: bool = False) -> list:
        """This func synchronizate client and server"""

        for element in os.listdir(config.CLIENT_DIRECTORY + current_path):
            #Check folder
            if os.path.isdir(config.CLIENT_DIRECTORY + current_path + element):
                self.Client_Class.Add_Folder(current_path + element)
                output = self.syn(current_path + element + "\\\\")
                continue
            #File is be

            res, wei = self.Client_Class.Add_File(element, current_path)
            if res.status_code == 200:
                 self.Data["Add elements"] = list(self.Data["Add elements"]) + [[element, wei]]
                 continue

            response = self.Client_Class.Check_File(element, current_path)
            if response.text == "True":
                
                self.Client_Class.Change_File(element, current_path)
                path = config.CLIENT_DIRECTORY + current_path + element
                size = os.path.getsize(path)
                self.Data["Change elements"] = list(self.Data["Change elements"]) + [[element, size]]

            
            
            
            

        #was File remover
        removed_names: list[str] = self.Client_Class.Check_Removed(os.listdir(config.CLIENT_DIRECTORY + current_path), current_path)
        for removed_name in removed_names:
            # Remove file
            res = self.Client_Class.Remove_File(removed_name, current_path)
            try:
                size = int(res.text)
            except ValueError as e:
                size = 0
            self.Data["Remove elements"] = list(self.Data["Remove elements"]) + [[removed_name, size]]
            

class Server:
    def __init__(self) -> None:
        self.Server_Class = server.Server(config.PORT)

    def Get_Info(self):
        return self.Server_Class.Get_Info()

    def Run(self):
        self.Server_Class.Start_Server()









