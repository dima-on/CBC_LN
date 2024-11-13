import os
import socket
import flask
from Backend import synchronization
import time
import json
from datetime import datetime
from Info import config
import shutil
from Backend import dop
import logging

app = flask.Flask(__name__)
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


class Server:
    """Class for controll of server"""

    def __init__(self, port: int) -> None:
        """
        :param port: which port will be using
        """
        path = config.SERVER_DIRECTORY + ".info"
        if (
            synchronization.Checker(config.SERVER_DIRECTORY).File_Is_Be(".info")
            == False
        ):
            os.mkdir(path)
            with open(str(path) + "\\" + "data.json", "w") as json_file:
                json.dump({}, json_file)
                config.DATA_PATH = str(path) + "\\" + "data.json"
        else:
            config.DATA_PATH = str(path) + "\\" + "data.json"

        self.Port = port

    def Start_Server(self):
        app.run(host="0.0.0.0", port=self.Port)

    def Get_Info(self) -> tuple[str, int]:

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        return ip_address, self.Port

    @app.route("/" + config.PATH_NAME["Add File"], methods=["POST"])
    def Add_File():
        """
        Add file only on the server \n
        param: file and name of file
        """

        file = flask.request.files["file"]
        name = flask.request.form.get("name")
        current_path = flask.request.form.get("current path")

        dop.start_file(name)

        checker = synchronization.Checker(path=config.SERVER_DIRECTORY + current_path)
        if file:
            is_be = checker.File_Is_Be(name)
            if is_be == False:
                file.save(config.SERVER_DIRECTORY + current_path + name)
                dop.end_file(name)

                data_class = synchronization.Data(config.DATA_PATH)
                data_class.Write_Data(
                    "Add File", (data_class.Get_Normal_Time(time.time()), name)
                )

                return "file have been saved", 200
            else:
                return "file already have been added", 201

        else:
            return "dont have file", 401

    @app.route("/" + config.PATH_NAME["Remove File"], methods=["POST"])
    def Remove_File():
        """
        Remove file only on the server \n
        param: name file
        """
        name = flask.request.form.get("name")
        current_path = flask.request.form.get("current_path")
        size = 0

        if current_path != ".info" and name != ".info":

            path = config.SERVER_DIRECTORY + current_path + name
            checker = synchronization.Checker(
                path=config.SERVER_DIRECTORY + current_path
            )
            is_be = checker.File_Is_Be(name)

            if is_be == True:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    size = os.path.getsize(path)
                    os.remove(path)

                # data_class = synchronization.Data(config.DATA_PATH)
                # data_class.Write_Data(
                #     "Remove File", (data_class.Get_Normal_Time(time.time()), name)
                # )

                return str(size), 200

            else:
                return "file havent been founded", 400
        else:
            return "it is hide folder", 201

    @app.route("/" + config.PATH_NAME["Change File"], methods=["POST"])
    def Change_File():
        """
        Change file only on the Server \n
        param: file, name of file
        """
        file = flask.request.files["file"]
        name = flask.request.form.get("name")
        current_path = flask.request.form.get("current path")

        dop.start_file(name)

        checker = synchronization.Checker(path=config.SERVER_DIRECTORY + current_path)
        if file:
            is_be = checker.File_Is_Be(name)
            if is_be:
                file.save(config.SERVER_DIRECTORY + current_path + name)
                dop.end_file(name)
                # data_class = synchronization.Data(config.DATA_PATH)
                # data_class.Write_Data(
                #     "Change File", (data_class.Get_Normal_Time(time.time()), name)
                # )

                return "file have been changed", 200
            else:
                return "file havent been founded", 400

        else:
            return "dont have file", 400

    @app.route("/" + config.PATH_NAME["Check File"], methods=["GET"])
    def Check_File():
        """
        Check file if it be then \n
        return True else return False
        """
        file = flask.request.files["file"]
        name = flask.request.form.get("name")
        current_path = flask.request.form.get("current path")
        type_check = int(flask.request.form.get("type check"))
        
        checker = synchronization.Checker(path=(config.SERVER_DIRECTORY + current_path).replace("\\\\", "\\") )
        if file:
            is_be = checker.File_Is_Be(name)
            if type_check == 0:
                return str(is_be), 200
            
            if type_check == 1:
                if is_be:
                    
                    if checker.Check_Changes(file_name=name, new_file=file):
                        return "True", 200
                    else:
                        return "False", 200
            return "Non Type", 400

        return "Error", 400

    @app.route("/" + config.PATH_NAME["Add Folder"], methods=["POST"])
    def Add_Folder():
        name = flask.request.form.get("name")
        path = config.SERVER_DIRECTORY + name

        if not os.path.exists(path):
            os.makedirs(path)

        return "yes", 200

    @app.route("/" + config.PATH_NAME["Check Removed"], methods=["GET"])
    def Check_Removed():
        """
        Check be file on the server which is not on the client \n
        return array with names file which is not on the client
        """
        names: str = flask.request.form.get("names")
        current_path: str = flask.request.form.get("current_path")

        names = eval(names)

        removed_names: list[str] = []

        for element in os.listdir(config.SERVER_DIRECTORY + current_path):
            Was_Removed: bool = True

            for name in names:
                if name == element:
                    Was_Removed = False

            if Was_Removed:
                removed_names.append(element)

        return str(removed_names), 200

    @app.route("/" + config.PATH_NAME["Get Status"], methods=["GET"])
    def Get_Status():
        """return info"""
        return synchronization.Data(config.DATA_PATH).Read_Data(), 200
