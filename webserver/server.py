import socket

HOST = ''
PORT = 8888
response = "HTTP/1.1 200 OK\n"\
           "Content-Type: text/html\n"\
           "\n"\
           "<html><body>Hello World</body></html>\n"

another_response = "HTTP/1.1 200 OK\r\nContent-Length: 13\r\nConnection: close\r\n\r\nHello, world!"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f"serving on: {PORT}")
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        while True:
            data = conn.recv(1024)
            if not data: break
            import pdb; pdb.set_trace()
            conn.send(another_response.encode())
