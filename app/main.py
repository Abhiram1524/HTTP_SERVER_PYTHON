import socket

def main():
    print("Logs from your program will appear here!")

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

        # Check if the path starts with /echo/
        if path.startswith('/echo/'):
            # Extract the string after /echo/
            echo_string = path[len('/echo/'):]
            content_length = len(echo_string)
            http_response = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: text/plain\r\n"
                f"Content-Length: {content_length}\r\n\r\n"
                f"{echo_string}"
            )
        else:
            http_response = "HTTP/1.1 404 Not Found\r\n\r\n"

        # Send the HTTP response
        client_socket.sendall(http_response.encode())

        # Close the client connection
        client_socket.close()

if __name__ == "__main__":
    main()
