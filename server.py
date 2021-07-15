#!/usr/bin/python3
# -*- coding:utf8 -*-

from os.path import exists, splitext, join, dirname, abspath, realpath, basename
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
import cgi


class ServerHttp(BaseHTTPRequestHandler):

    def __init__(self, public_folder, *args):
        self._root = dirname(abspath(__file__))
        self._public = realpath(join(self._root, public_folder))
        self._commands = {
            'close_server': self.__exit,
        }

        BaseHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
        if self.__is_file(self.path):
            if self.path == '/':
                file_name = self._public + '/index.html'
            else:
                file_name = self._public + self.path
        
            with open(file_name, 'rb') as fh:
                dat = fh.read()
                if '.html' in file_name:
                    dat = self.__add_button_close_server(dat)    
                self.__answer(200, self.__mimetype(file_name), dat)

        elif self.__is_command(self.path):
            self.__do_command(self.path)
        else:
            r = f'"{self.path}" :( '.encode('utf-8')
            self.__answer(200, self.__mimetype('.txt'), r)
    
    def do_POST(self):
        ped = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        ac = ped.getvalue('action')

        r = ''.encode('utf-8')
        self.__answer(200, self.__mimetype('.txt'), r) 

    def __is_file(self, v):
        r =  realpath(join(self._public, v.strip('/')))
        return exists(r)

    def __is_command(self, v):
        v = v.split('?')[0]
        print(v)
        return v.strip('/') in self._commands

    def __do_command(self, v):
        s = '?'
        v = v.strip('/')
        if s in v:
            cmd, args = v.split(s)
            self._commands[cmd](args)
        else:
            self._commands[v]()

    def __exit(self):
        self.__answer(200, self.__mimetype('.txt'), ':)'.encode('utf-8'))
        server_stop()

    def __answer(self, status, mime, data):
        self.send_response(status)
        self.send_header('Content-type', mime)
        self.end_headers()
        self.wfile.write(data)

    def __mimetype(self, file_name='', default='.txt'):
        _, ext = splitext(file_name)
        mime = {
         '.css': 'text/css',
         '.json': 'application/javascript',
         '.js': 'application/javascript',
         '.txt': 'text/plain',
         '.html': 'text/html',
         '.md': 'text/plain',
         '.yml': 'text/plain',
         '.svg': 'image/svg+xml',
         '.jpg': 'image/jpeg',
         '.png': 'image/png',
         '.ico': 'image/x-icon',
        }
        if not ext in mime:
            ext = default
        return mime[ext]

    def __add_button_close_server(self, dat):
        tex = dat.decode('utf-8')
        pin = '</body>'
        add = '''
        <style>
            #btn_close_server {
                font-size:.9em;
                padding:4px 8px;
                text-decoration:none;
                position:fixed;
                bottom:0;
                right:0;
                cursor:pointer;
                opacity:.7;
                border:0;
                margin:3px;
                border:1px solid #aaa;
            }
            #btn_close_server:hover {
                opacity:1;
            }
        </style>
        <script>
            function server_close(){
                $.get('/close_server', function(r){
                    window.close();
                });
            }
        </script>
        <button id="btn_close_server" href="/exit" onclick="server_close()">EXIT</button>
        '''
        return tex.replace(pin, f'{add}{pin}').encode('utf-8')

def server(public_folder='./', host='localhost', port=8000):

    def handler(*args):
        ServerHttp(public_folder, *args)

    httpd = HTTPServer((host, port), handler)

    url = f'http://{host}:{port}/'

    def start():
        print('Starting httpd on port {}'.format(port))
        httpd.serve_forever()

    def stop():
        sys.exit()

    return url, start, stop


if __name__ == '__main__':
    url, server_start, server_stop = server(public_folder='./public_html/', port=8081)
    webbrowser.open_new_tab(url)
    server_start()