import socket
import threading
import argparse
import os
FILE_DIR = ""
def create_headers(headers: dict):
    return "\r\n".join([f"{k}: {v}" for k, v in headers.items()])
def create_response(client, status: str, headers: dict, body: bytes):
    resp = f"HTTP/1.1 {status}\r\n"
    if len(headers) > 0:
        resp += create_headers(headers) + "\r\n"
    resp += "\r\n"
    if len(body) > 0:
        resp += body.decode()
    client.send(resp.encode())
    client.close()
    return
def extract_headers(data):
    values = {}
    for d in data:
        k = d.split(":")[0]
        v = d[len(k) + 2 :]
        v = v.replace("\r\n", "")
        values[k] = v
    return values
def handle_client(client):
    global FILE_DIR
    data = client.recv(1024)
    if b"\r\n\r\n" not in data:
        client.close()
        return
    header_data = data[: data.find(b"\r\n\r\n")].decode().split("\r\n")
    body_data = data[data.find(b"\r\n\r\n") + 4 :]
    headers = extract_headers(header_data[1:])
    path_data = header_data[0].split(" ")
Expand 26 lines
                )
            if path_type == "POST":
                return
                with open(p, "wb") as out:
                    out.write(body_data)
            return
                client.send("HTTP/1.1 201 OK\r\n\r\n".encode())
                client.close()
                return
        if "/echo/" in path_path:
            echo = path_path[path_path.find("/echo/") + 6 :]
            return create_response(
                client,
                "200 OK",
                {"Content-Type": "text/plain", "Content-Length": len(echo)},
                echo.encode(),
            )
        if "/user-agent" in path_path:
            return create_response(
                client,
                "200 OK",
                {
                    "Content-Type": "text/plain",
                    "Content-Length": len(headers["User-Agent"]),
                },
                headers["User-Agent"].encode(),
            )
        client.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        client.close()
        return
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory")
    args = parser.parse_args()
    if "directory" in args:
        global FILE_DIR
        FILE_DIR = args.directory
    server_socket = socket.create_server(("localhost", 4221))  # , reuse_port=True
    while True:
        client, _ = server_socket.accept()  # wait for client
        threading.Thread(target=handle_client, args=(client,)).start()
if __name__ == "__main__":
    main()