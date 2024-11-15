import pytest
from unittest.mock import patch, MagicMock, ANY, call
from Interface.main import Server, Client

@pytest.fixture
def patch_check_file():
    with patch("Backend.connect.Connect.Check_File") as mock:
        yield mock


@pytest.fixture
def patch_add_file():
    with patch("Backend.connect.Connect.Add_File") as mock:
        yield mock


@pytest.fixture
def patch_change_file():
    with patch("Backend.connect.Connect.Change_File") as mock:
        yield mock

@pytest.fixture
def patch_check_removed():
    with patch("Backend.connect.Connect.Check_Removed") as mock:
        yield mock


@pytest.fixture
def patch_remove_file():
    with patch("Backend.connect.Connect.Remove_File") as mock:
        yield mock

@pytest.fixture
def patch_add_folder():
    with patch("Backend.connect.Connect.Add_Folder") as mock:
        yield mock

def mock_fun_empty(*args, **kwargs):
    pass

def test_get_full_size(patch_check_file):
    mock_response = MagicMock()
    mock_response.text = "False"
    patch_check_file.return_value = mock_response
    current_path = "C:\\Users\\sinic\\Python_Project\\CBC_LN\\tests\\test_file\\Client\\"
    client = Client([mock_fun_empty, mock_fun_empty])

    size = client.Get_Full_Size(current_path=current_path)

    patch_check_file.assert_called_once_with(
        ANY,
        ANY,
        0
    )

    assert size >= 0

def test_syn(patch_check_file, 
             patch_add_file, 
             patch_change_file,
             patch_check_removed,
             patch_remove_file,
             patch_add_folder):
    

    mock_response = MagicMock()
    mock_response.text = "True"
    patch_check_file.return_value = mock_response

    mock_response = MagicMock()
    mock_response.status_code = 200
    patch_add_file.return_value = (mock_response, 100)


    mock_response = MagicMock()
    mock_response.status_code = 200
    patch_change_file.return_value = mock_response

    patch_check_removed.return_value = ["test.txt", "test1.txt"]

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "100"
    patch_remove_file.return_value = mock_response

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "Ok"
    patch_add_folder.return_value = mock_response




    current_path = "C:\\Users\\sinic\\Python_Project\\CBC_LN\\tests\\test_file\\Client\\"
    client = Client([mock_fun_empty, mock_fun_empty])
    client.Size = 500
    client.Current_Size = 500

    

    client.syn(current_path=current_path)