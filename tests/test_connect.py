import pytest
from unittest.mock import patch, MagicMock, ANY, call
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Backend.connect import Connect

# Фикстура для замены requests.post
@pytest.fixture
def mock_post():
    with patch('requests.post') as mock:
        yield mock

@pytest.fixture
def mock_get():
    with patch('requests.get') as mock:
        yield mock


def test_add_file(mock_post):

    ip = 'http://localhost'
    commands = {'Add File': 'Add_File'}
    file_name = 'test.txt'
    current_path = 'C:\\Users\\sinic\\Python_Project\\CBC_LN\\tests\\test_file\\Client\\'


    # Настраиваем фиктивный ответ
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = 'Success'
    mock_post.return_value = mock_response


    connect = Connect(ip, commands)

    response, file_size = connect.Add_File(file_name, current_path)


    # Проверяем вызов mock_post
    mock_post.assert_called_once_with(
        url=f'{ip}/{commands["Add File"]}',
        files={'file': ANY},
        data={'name': file_name, 'current path': current_path}
    )

    assert response.status_code == 200

def test_remove_file(mock_post):
    # Настраиваем фиктивный ответ
    mock_response = MagicMock()
    mock_response.status_code = 200  # Реальный статус код
    mock_response.text = 'File removed'  # Можете настроить как нужно
    mock_post.return_value = mock_response


    ip = 'http://localhost'
    commands = {'Remove File': 'Remove_File'}
    file_path = 'test.txt'
    current_path = 'C:\\Users\\sinic\\Python_Project\\CBC_LN\\tests\\test_file\\Client\\'
    
    # Создаем объект Connect
    connect = Connect(ip, commands)
   
    response = connect.Remove_File(file_path, current_path)
    
    
    mock_post.assert_called_once_with(
        url=f'{ip}/{commands["Remove File"]}',
        data={'name': file_path, 'current_path': current_path}
    )

    # Проверяем, что код состояния ответа равен 200
    assert response.status_code == 200

def test_change_file(mock_post):
    # Настраиваем фиктивный ответ
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = 'True'
    mock_post.return_value = mock_response

    # Настройка параметров
    ip = 'http://localhost'
    commands = {'Change File': 'Change_File'}
    file_name = 'test.txt'
    current_path = 'C:\\Users\\sinic\\Python_Project\\CBC_LN\\tests\\test_file\\Client\\'
    
    # Создаем объект Connect
    connect = Connect(ip, commands)
    
    # mock_response = MagicMock()
    # mock_response = open(current_path, "r")
    # mock_post.return_value = mock_response

    # Вызываем метод Add_File
    response = connect.Change_File(file_name, current_path)

    
    # Проверяем, что open был вызван с правильным путем к файлу и режимом 'rb'
    #mock_open.assert_called_once_with(file_path, 'rb')

    # Проверяем вызов mock_post
    mock_post.assert_called_once_with(
        url=f'{ip}/{commands["Change File"]}',
        files={'file': ANY},  # Используем ANY для обозначения файла
        data={"name": file_name, "current path": current_path}
    )

    # Проверяем, что код состояния ответа равен 200
    assert response == "True"

def test_add_folder(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = 'True'
    mock_post.return_value = mock_response

    # Настройка параметров
    ip = 'http://localhost'
    commands = {'Add Folder': 'Add_Folder'}
    file_path = 'test_path'


    connect = Connect(ip=ip, comands_names=commands)
    response = connect.Add_Folder(file_path)

    mock_post.assert_called_once_with(
        url=f'{ip}/{commands["Add Folder"]}',
        data={"name": file_path}
    )

    assert response.status_code == 200

def test_get_removed_file(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = str(["test.txt"])
    mock_get.return_value = mock_response

    # Настройка параметров
    ip = 'http://localhost'
    commands = {'Check Removed': 'Check_Removed'}
    file_names = ['test_path', "second.txt"]
    current_path = "\\Client"

    connect = Connect(ip=ip, comands_names=commands)

    response = connect.Check_Removed(file_names=file_names, current_path=current_path)

    mock_get.assert_called_once_with(
        url=f'{ip}/{commands["Check Removed"]}',
        data={
            "names": str(file_names),
            "current_path": current_path
        }
    )

    assert response == ["test.txt"]

def test_check_file(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "True"
    mock_get.return_value = mock_response

    # Настройка параметров
    ip = 'http://localhost'
    commands = {'Check File': 'Check_File'}
    file_name = "test.txt"
    full_path = "C:\\Users\\sinic\\Python_Project\\CBC_LN\\tests\\test_file\\Client\\"


    connect = Connect(ip=ip, comands_names=commands)

   
    responce_0 = connect.Check_File(file_name=file_name, current_path=full_path, type_check=0)
    responce_1 = connect.Check_File(file_name=file_name, current_path=full_path, type_check=1)

    
    mock_get.assert_has_calls([
            call(
                url=f'{ip}/{commands["Check File"]}',
                files={'file': ANY},
                data={"name": file_name, "current path": full_path, "type check": 0},
                timeout=ANY
            ),
            call(
                url=f'{ip}/{commands["Check File"]}',
                files={'file': ANY},
                data={"name": file_name, "current path": full_path, "type check": 1},
                timeout=ANY
            )
        ], any_order=False)

    assert responce_0.text == "True"
    assert responce_0.status_code == 200
    assert responce_1.text == "True"
    assert responce_1.status_code == 200





# @pytest.fixture
# def test_fict():
#     print("tesst")
#     yield 15
#     print("end")

# def test_tests(test_fict):
#     print(test_fict)


# @pytest.fixture
# def mock_open_fixture():
#     # Патчим open для теста
#     with patch("builtins.open", mock_open(read_data="some content")) as mock:
#         print("mock_open_fixture started")
#         yield mock
#         print("mock_open_fixture ended")
        

# def test_file_open(mock_open_fixture):
#     # Здесь mock_openFixture уже замещает open
#     print("test_file_open started")
#     with open("C:\\Users\\sinic\\Python_Project\\CBC_LN\\tests\\test_file\\Client\\test.txt", "r") as file:
#         content = file.read()

#     print(f"Content: {content}")
    
#     # Проверка
#     assert content == "some content"
#     mock_open_fixture.assert_called_with("C:\\Users\\sinic\\Python_Project\\CBC_LN\\tests\\test_file\\Client\\test.txt", "r")
#     print("test_file_open ended")
# Тест для метода Add_File


# @pytest.fixture
# def switch_out():
#     with patch("Backend.dop.test_to_work") as mock:
#         yield mock
    
# def test_trs(switch_out):
#     from Backend.dop import test_to_work
#     switch_out.return_value = 15
#     t = test_to_work()
#     assert t == 15
