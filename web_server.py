import socket

def get_response(request: list[str]) -> bytes:
    file_path = request[0].split()[1][1::]
    if file_path == "": file_path = "index.html"
    file_ext = file_path.split(".")[1]
    if file_ext == "html":
        file_type = "text/html"
    elif file_ext == "css":
        file_type = "text/css"
    elif file_ext == "js":
        file_type = "application/javascript"
    elif file_ext == "jpg":
        file_type = "image/jpeg"
    elif file_ext == "gif":
        file_type = "image/gif"
    elif file_ext == "png":
        file_type = "image/png"
    else: file_type = None

    try:
        file = open(file_path, "r+b")
        code = (200, "OK")
    except FileExistsError:
        file = open("404.html", "r+b")
        code = (404, "Not found")
    file_content = file.read()
    res: bytes = \
        f"HTTP/1.1 {code[0]} {code[1]}\r\nContent-Type: {file_type}\r\nContent-Length: {len(file_content)}\r\n\r\n".encode() + file_content
    return res

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 80))
server_socket.listen()
# req size = 1024
while True:
    client_socket, address = server_socket.accept()
    req: str = client_socket.recv(1024).decode()
    sep = req.split("\r\n")
    response = get_response(sep)
    print(req)
    print("---")
    print(sep)
    print("---")
    print(response)

    client_socket.send(response)
    client_socket.close()

