import unittest
from unittest.mock import MagicMock
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Backend.server import app  # Импортируем ваше Flask-приложение

def test_add_file():
    client = app.test_client()
    client.testing = True

    file_data = {'file': (MagicMock(), 'test.txt')}  # Используем MagicMock вместо реального файла
    form_data = {
        'name': 'test.txt',
        'current path': 'C:\\Users\\sinic\\Python_Project\\CBC_LN\\tests\\test_file\\Client\\'
    }

        # Отправляем POST-запрос с файлом и данными формы
    response = client.post(
            "/Add_File",
            data={**form_data, **file_data},  # Используем объединение данных формы и файла
            content_type='multipart/form-data',  # Указываем тип контента
            follow_redirects=True
        )

    # Выводим ответ для отладки

    assert response.status_code == 200 or response.status_code == 201

def test_change_file():
    client = app.test_client()
    client.testing = True

    file_data = {'file': (MagicMock(), 'test.txt')}  # Используем MagicMock вместо реального файла
    form_data = {
        'name': 'test.txt',
        'current path': 'C:\\Users\\sinic\\Python_Project\\CBC_LN\\tests\\test_file\\Client\\'
    }

        # Отправляем POST-запрос с файлом и данными формы
    response = client.post(
            "/Change_File",
            data={**form_data, **file_data},  # Используем объединение данных формы и файла
            follow_redirects=True
        )

    # Выводим ответ для отладки

    assert response.status_code == 200 or response.status_code == 201

def test_check_removed():
    client = app.test_client()
    client.testing = True

    form_data = {
        'names': str(['test.txt']),
        'current_path': 'C:\\Users\\sinic\\Python_Project\\CBC_LN\\tests\\test_file\\Client\\'
    }

    response = client.get(
            "/Check_Removed",
            data={**form_data},  # Используем объединение данных формы и файла
            follow_redirects=True
        )


    assert response.status_code == 200 or response.status_code == 201

def test_check_file():
    client = app.test_client()
    client.testing = True
    current_path = "C:\\Users\\sinic\\Python_Project\\CBC_LN\\tests\\test_file\\Client\\"
    name = "test.txt"
    form_data = {
        'name': name,
        'current path': current_path,
        "type check": 0
    }
    from_file = {'file': (MagicMock(), name)}
    

    response = client.get(
            "/Check_File",
            data={**form_data, **from_file},  # Используем объединение данных формы и файла
            follow_redirects=True
        )
    assert response.status_code == 200 or response.status_code == 201

    form_data = {
        'name': name,
        'current path': current_path,
        "type check": 1
    }
    with open(current_path + name, "rb")as file:
        from_file = {'file': file}
        response = client.get(
                "/Check_File",
                data={**form_data, **from_file},  # Используем объединение данных формы и файла
                follow_redirects=True
            )


    assert response.status_code == 200 or response.status_code == 201
