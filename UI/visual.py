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
def Set_Proc(proc):
    eel.Set_Proces(proc)

@eel.expose
def Add_Block(element, wei):
    eel.Add_elements([element, wei], ".client .log .Add_elements")


def Delegate_Proces(Proc: int) -> None:
    Set_Proc(Proc)

def Delegate_Add_Block(element: str, wei: int) -> None:
    Add_Block(element, wei)

@eel.expose
def Get_Full_Size(link: str, path: str) -> float:
    config.IP = link
    config.CLIENT_DIRECTORY = Refactor_Path(path)
    client = main.Client(func=[Delegate_Proces, Delegate_Add_Block])
    Full_size = client.Get_Full_Size()

    return Full_size

@eel.expose
def Synchronizate_Fun(Size: float) -> dict:
    client = main.Client(func=[Delegate_Proces, Delegate_Add_Block])
    client.Current_Size = Size
    client.Size = Size


    st = time.time()
    client.syn()
    print(time.time() - st)
    return client.Data


# Запуск веб-приложения
eel.start("index.html", port=809, size=(500, 500))
