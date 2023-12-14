from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
import json
import socket
from threading import Thread 
from datetime import datetime 



UDP_IP = '127.0.0.1'
UDP_PORT = 5000

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def do_POST(self):
        print("do_POST:")
        data = self.rfile.read(int(self.headers['Content-Length']))
        self.send_new_data(data)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def send_new_data(self, data):
        print("send_new_data: create socket client")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server = UDP_IP, UDP_PORT
        sock.sendto(data, server)
        sock.close()


def run_HTTP(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()



def run_socket_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = UDP_IP, UDP_PORT
    sock.bind(server)
    dfile = pathlib.Path.cwd() / "storage" / "data.json"
    try:
        while True:
            data, _ = sock.recvfrom(1024)
            if len(data) > 0:
                data_parse = urllib.parse.unquote_plus(data.decode())
                data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}   
                if len(data_dict.get("username", 0)) and len(data_dict.get("message", 0)):
                    with open(dfile, "r") as fh:
                        users = json.load(fh)

                    today = datetime.today()
                    new = {str(today): {"username": data_dict["username"], "message": data_dict["message"]}}
                    users.update(new)

                    with open(dfile, "w") as fh:
                        json.dump(users, fh)
    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        sock.close()



if __name__ == '__main__':
    
    t1 = Thread(target = run_socket_server)
    t1.start()

    t2 = Thread(target = run_HTTP)
    t2.start()
