# Project Documentation

## Description
This project is a client-server application for file synchronization. The client side sends data to the server, which manages files, checks their existence and changes, and provides functionality for adding and deleting files and folders.

---

## Core Modules

### `visual.py`
The main file for running the application using the `eel` library to interact with an HTML interface.

#### Key Functions:
- `Start_Server()`: Starts the server.
- `Get_Info(port, path)`: Returns server information (IP and port) for the given path and port.
- `Get_Full_Size(link, path)`: Calculates the total size of files to be synchronized.
- `Synchronizate_Fun(Size)`: Synchronizes the client directory with the server.

---

### `main.py`
A module containing classes for the client and server, along with utilities for handling paths.

#### Class `Client`
Handles interaction with the server and manages client files.

- `__init__(func)`: Initializes the client, configuring the connection and data.
- `Get_Full_Size(current_path)`: Calculates the total size of files in a directory.
- `syn(current_path)`: Synchronizes client files with the server.

#### Class `Server`
Provides functionality for starting and managing the server.

- `__init__()`: Initializes the server.
- `Get_Info()`: Returns server information (IP and port).
- `Run()`: Starts the server.

#### Utility `Refactor_Path(path)`
Converts the path to a standard format by adding backslashes.

---

### `server.py`
Implements the server-side logic using Flask.

#### Class `Server`
- `Start_Server()`: Starts the Flask server.
- `Get_Info()`: Returns the server's IP address and port.

#### Key Routes:
- `POST /Add File`: Adds a file to the server.
- `POST /Remove File`: Deletes a file from the server.
- `POST /Change File`: Updates a file on the server.
- `GET /Check File`: Checks for a file's existence on the server.
- `POST /Add Folder`: Adds a folder to the server.
- `GET /Check Removed`: Checks for missing files on the client.
- `GET /Get Status`: Returns the server's status.

---

### `synchronization.py`
A module for handling file synchronization and validation.

#### Class `Checker`
- `File_Is_Be(file_name)`: Checks if a file exists in the specified directory.
- `Check_Changes(file_name, new_file)`: Compares a new file with the existing one for changes.
- `Get_File_Hash(file)`: Returns the file's hash.

#### Class `Data`
- `Write_Data(key, value)`: Writes data to a JSON file (implementation commented out).
- `Read_Data()`: Reads data from a JSON file (implementation commented out).
- `Get_Normal_Time(time)`: Converts a timestamp to the format `YYYY-MM-DD HH:MM:SS`.

---

## Installation and Running

1. Install dependencies:
   ```bash
   pip install -r requirements.txt



2. Start the app:

   ```bash
   python visual.py


---

## API Usage Examples

### Add File

**Route**: `POST /Add File`  
**Parameters**:

- `file`: File to upload to the server.  
- `name`: File name.  
- `current path`: Current path.  

**Responses**:

- `200`: File successfully added.  
- `201`: File already exists.  
- `401`: Error uploading the file.  

---

### Check File

**Route**: `GET /Check File`  
**Parameters**:

- `name`: File name.  
- `current path`: Current path.  
- `type check`: Check type (`0` or `1`).  

**Responses**:

- `200`: Successful check.  
- `400`: Invalid request.  
