import eel
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import Interface.main as main


from Info import config

# Указываем путь к папке с HTML-файлами
eel.init("UI/web")


def Refactor_Path(path: str) -> str:
    return path.replace("\\", "\\\\") + "\\\\"


@eel.expose
def Start_Server():
    server = main.Server()
    server.Run()


@eel.expose
def Get_Info(port: int, path: str):

    config.PORT = port
    config.SERVER_DIRECTORY = Refactor_Path(path)

    server = main.Server()

    ip, port = server.Get_Info()
    link = "http://" + str(ip) + ":" + str(port)

    return link


@eel.expose
def Synchronizate_Fun(link: str, path: str):
    config.IP = link
    config.CLIENT_DIRECTORY = Refactor_Path(path)
    client = main.Client()
    st = time.time()
    client.syn(is_First=True)
    print(time.time() - st)
    return client.Data


# Запуск веб-приложения
eel.start("index.html", port=809, size=(500, 500))
