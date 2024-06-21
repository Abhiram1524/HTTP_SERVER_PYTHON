import socket
import threading
import sys
import os

def handle_req(client, addr, directory):
    try:
        data = client.recv(1024).decode()
        req = data.split("\r\n")
        request_line = req[0].split(" ")
        method = request_line[0]
        path = request_line[1]

        if method == "GET" and path.startswith("/files/"):
            filename = path[len("/files/"):]
            file_path = os.path.join(directory, filename)

            if os.path.isfile(file_path):
                with open(file_path, "r") as f:
                    body = f.read()

                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

        client.send(response)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

def main():
    if len(sys.argv) != 3 or sys.argv[1] != '--directory':
        print("Usage: ./your_server.sh --directory /path/to/files")
        return

    directory = sys.argv[2]
    if not os.path.isdir(directory):
        print(f"Directory {directory} does not exist.")
        return

    try:
        server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
        print("Server is listening on port 4221")

        while True:
            client, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            threading.Thread(target=handle_req, args=(client, addr, directory)).start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
