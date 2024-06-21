import socket
import os
import sys

def main():
    print("Logs from your program will appear here!")

    # Parse the --directory flag to get the directory path
    if len(sys.argv) != 3 or sys.argv[1] != '--directory':
        print("Usage: ./your_server.sh --directory /path/to/files")
        return
    files_directory = sys.argv[2]

    # Create and bind the server socket
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen()
    print("Server is listening on port 4221")

    while True:
        # Accept a connection from a client
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Receive the request
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
            # Extract the filename from the path
            filename = path[len('/files/'):]
            file_path = os.path.join(files_directory, filename)

            if os.path.exists(file_path):
                # File exists, read its contents
                with open(file_path, 'rb') as file:
                    file_contents = file.read()
                content_length = len(file_contents)
                http_response = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: application/octet-stream\r\n"
                    f"Content-Length: {content_length}\r\n\r\n"
                ).encode() + file_contents
            else:
                # File does not exist
                http_response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        else:
            http_response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

        # Send the HTTP response
        client_socket.sendall(http_response)

        # Close the client connection
        client_socket.close()

if __name__ == "__main__":
    main()
