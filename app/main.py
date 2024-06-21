import socket
import os
import sys
import threading

# Define a global variable for the files directory
files_directory = None

def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode()
        print(f"Received request: {request}")

        # Parse the request line
        request_line = request.split('\r\n')[0]
        print(f"Request line: {request_line}")

        # Extract the method and URL path
        method, path, _ = request_line.split(' ')
        print(f"Method: {method}, Path: {path}")

        # Determine the response based on the URL path
        if path.startswith('/files/'):
            filename = path[len('/files/'):]
            file_path = os.path.join(files_directory, filename)

            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    file_contents = file.read()
                content_length = len(file_contents)
                http_response = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: application/octet-stream\r\n"
                    f"Content-Length: {content_length}\r\n\r\n"
                ).encode() + file_contents
            else:
                http_response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        else:
            http_response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

        client_socket.sendall(http_response)
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def main():
    global files_directory
    print("Logs from your program will appear here!")

    # Check if the correct number of arguments are provided
    if len(sys.argv) != 3 or sys.argv[1] != '--directory':
        print("Usage: ./your_server.sh --directory /path/to/files")
        return
    
    # Set the files directory
    files_directory = sys.argv[2]

    # Create a TCP/IP socket
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen()
    print("Server is listening on port 4221")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()
