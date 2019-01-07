#!/usr/bin/env python
#-*- coding: utf-8 -*-

import socket
import sys
import functools

class BassoonApp(object):
    """ A toy framwork """

    def __init__(self):
        self.routes = []

    def __call__(self, environ, start_response):
        request_method = environ['REQUEST_METHOD']
        path_info      = environ['PATH_INFO']

        if path_info[-1] == "/":
            path_info = path_info[:-1]

        for route in self.routes:
            if route.method == request_method and route.path == path_info:
                start_response('200 OK', [('Content-Type', 'text/html')])
                return route.callback()
        start_response('404 Not found', [('Content-Type', 'text/html')])
        return "not found"

    def __add_route(self, route):
        self.routes.append(route)

    def route(self, path, method):
        if path[-1] == "/":
            path = path[:-1]

        def wrapper(callback):
            route = BassoonRoute(path, method, callback)
            self.__add_route(route)
            return callback
        return wrapper

    def get(self, path, method="GET"):
        return self.route(path, method)

    def post(self, path, method="POST"):
        return self.route(path, method)

class BassoonRoute(object):
    """ Routes of BassoonApp """

    def __init__(self, path, method, callback):
        self.path     = path
        self.method   = method
        self.callback = callback

class BassoonServer(object):
    """ A toy server implemented WSGI protocal """

    __QUEUE_SIZE = 5
    __BUFF_SIZE  = 4096

    def __init__(self, host="localhost", port="8888", app=None):
        self.host = host
        self.port = port
        self.app  = app

        addr = (self.host, int(self.port))
        self.sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sckt.bind(addr)
        self.sckt.listen(self.__QUEUE_SIZE)

    def __read_socket(self):
        self.conn, addr = self.sckt.accept()
        req = ""
        while True:
            recv = self.conn.recv(self.__BUFF_SIZE)
            req += recv
            if len(recv) < self.__BUFF_SIZE:
                break
            elif req[-4:] == "\r\n\r\n":
                break
        return req

    def __parse_request(self, req):
        import StringIO, re

        req = req.split("\r\n")
        req = filter(lambda x: x, req)

        first_line = req.pop(0)
        print first_line
        request_method, request_path, request_version = first_line.split()

        environ = {}
        environ['wsgi.version']      = (1, 0)
        environ['wsgi.url_scheme']   = 'http'
        environ['wsgi.input']        = StringIO.StringIO(req)
        environ['wsgi.errors']       = sys.stderr
        environ['wsgi.multithread']  = False
        environ['wsgi.multiprocess'] = False
        environ['wsgi.run_once']     = False

        environ['REQUEST_METHOD']    = request_method
        environ['PATH_INFO']         = request_path
        environ['SERVER_NAME']       = self.host
        environ['SERVER_PORT']       = self.port

        for item in req:
            mc = re.search("(.+): (.+)", item)
            if not mc: continue
            key = mc.group(1)
            val = mc.group(2)
            environ[key] = val

        return environ

    def __start_response(self, status, header):
        self.response_set = [status, header]

    def __send_response(self, result):
        try:
            status, header = self.response_set
            response = 'HTTP/1.1 {status}\r\n'.format(status=status)
            response += '\r\n'
            for data in result:
                response += data
            self.conn.sendall(response)
        finally:
            self.conn.close()

    def handle_request(self):
        """ handle request once """

        req = self.__read_socket()
        environ = self.__parse_request(req)
        result = self.app(environ, self.__start_response)
        self.__send_response(result)

    def serve_forever(self):
        """ handle requests forever """

        print('BassoonServer: listening {host} on port {port} ...\n'.format(host=self.host, port=self.port))
        while True:
            self.handle_request()

def demo_app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return '<h1>Hello, web!</h1>'

def make_default_wrapper(attr):
    @functools.wraps(getattr(BassoonApp, attr))
    def wrapper(*a, **ka):
        return getattr(app, attr)(*a, **ka)
    return wrapper

app = BassoonApp()

get  = make_default_wrapper("get")
post = make_default_wrapper("post")

if __name__ == '__main__':
    bs = BassoonServer(host="0.0.0.0", port="8888", app=demo_app)
    bs.serverforever()




