import socket
import threading
import sys
import os

def handle_req(client, addr):
    try:
        req = client.recv(1024).decode().split("\r\n")
        print(req)
        reqline = req[0].split(" ")
        method = reqline[0]
        path = reqline[1]
        print(f"Method: {method}, Path: {path}")

        if path == "/":
            response = "HTTP/1.1 200 OK\r\n\r\n".encode()
        elif path.startswith("/echo"):
            message = path[6:]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(message)}\r\n\r\n{message}".encode()
        elif path.startswith("/user-agent"):
            for line in req:
                if line.startswith("User-Agent:"):
                    user_agent = line.split(": ")[1]
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()
                    break
        elif path.startswith("/files"):
            directory = sys.argv[2]
            filename = path[len("/files/"):]
            print(directory, filename)
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, "rb") as f:
                    body = f.read()
                response = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: application/octet-stream\r\n"
                    f"Content-Length: {len(body)}\r\n\r\n"
                ).encode() + body
            except FileNotFoundError:
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

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is listening on port 4221")
    
    while True:
        client, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        threading.Thread(target=handle_req, args=(client, addr)).start()

if __name__ == "__main__":
    main()
