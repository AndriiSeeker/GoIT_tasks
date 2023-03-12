from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from datetime import datetime
import socket
import urllib.parse
import pathlib
import mimetypes
import json
import logging

BASE_DIR = pathlib.Path()
BUFFER_SIZE = 1024
PORT_HTTP = 3000
SOCKET_HOST = '127.0.0.1'
SOCKET_PORT = 4000


def sent_data_to_socket(data):
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    c_socket.sendto(data, (SOCKET_HOST, SOCKET_PORT))
    c_socket.close()


class TheBestFastApp(BaseHTTPRequestHandler):

    def do_POST(self):
        length = self.headers.get('Content-Length')
        data = self.rfile.read(int(length))
        sent_data_to_socket(data)
        self.send_response(302)
        self.send_header('Location', r'message.html')
        self.end_headers()


    def do_GET(self):
        route = urllib.parse.urlparse(self.path)
        match route.path:
            case '/':
                self.send_html('index.html')
            case '/message':
                self.send_html('message.html')
            case _:
                file = BASE_DIR.joinpath(route.path[1:])
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html('error.html', 404)

    def send_html(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self, filename, status_code=200):
        self.send_response(status_code)
        mt = mimetypes.guess_type(filename)
        if mt:
            self.send_header('Content-type', mt[0])
        else:
            self.send_header('Content-type', 'text/plain')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())


def save_data_from_server(data):
    parse_data = urllib.parse.unquote_plus(data.decode())
    try:
        dict_parse = {key: value for key, value in [el.split('=') for el in parse_data.split('&')]}
        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        try:
            with open(r'storage/data.json', 'r', encoding='utf-8') as file:
                json_content = json.load(file)
        except json.decoder.JSONDecodeError:
            json_content = {}
        json_content.update({time: dict_parse})
        with open(r'storage/data.json', 'w', encoding='utf-8') as file:
            json.dump(json_content, file, ensure_ascii=False, indent=4)
            logging.debug(f"Info is written: {dict_parse}")
    except ValueError as err:
        logging.debug(f"For data {parse_data} error {err}")
    except OSError as err:
        logging.debug(f"Write data {parse_data} error {err}")


def run_socker_server(host, port):
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_socket.bind((host, port))
    try:
        while True:
            msg, address = s_socket.recvfrom(BUFFER_SIZE)
            save_data_from_server(msg)
    except KeyboardInterrupt:
        logging.info("Socker server stopped")
    finally:
        s_socket.close()


def run_server():
    address = ('0.0.0.0', PORT_HTTP)
    http = HTTPServer(address, TheBestFastApp)
    try:
        logging.info("Server is running")
        http.serve_forever()
    except KeyboardInterrupt:
        logging.info("Http server stopped")
    finally:
        http.server_close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")

    STORAGE_DIR = pathlib.Path().joinpath('storage')
    FILE_STORAGE = STORAGE_DIR / "data.json"
    if not FILE_STORAGE.exists():
        with open(FILE_STORAGE, 'w', encoding='utf-8') as file:
            json.dump({}, file, ensure_ascii=False)
            logging.debug(f"Json file is created")

    th_server = Thread(target=run_server)
    th_server.start()

    th_socket = Thread(target=run_socker_server, args=(SOCKET_HOST, SOCKET_PORT))
    th_socket.start()
