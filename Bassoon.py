#!/usr/bin/env python
#-*- coding: utf-8 -*-

import socket

class BassoonServer(object):
    __QUEUE_SIZE = 5
    __BUFF_SIZE  = 4096

    def __init__(self, host="localhost", port="8888", app=None):
        super(BassoonServer, self).__init__()
        self.sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        addr = (host, int(port))
        self.sckt.bind(addr)
        self.sckt.listen(self.__QUEUE_SIZE)

    def __read_socket(self):
        conn, addr = self.sckt.accept()
        req = ""
        while True:
            recv = conn.recv(self.__BUFF_SIZE)
            req += recv
            if len(recv) < self.__BUFF_SIZE:
                break
            elif req[-4:] == "\r\n\r\n":
                break
        conn.close()
        return req

    def __parse_request(self, req):
        import re
        req = req.split("\r\n")
        req = filter(lambda x: x, req)

        environ = {}
        first_line = req.pop(0)
        method = first_line.split()[0]
        environ["method"] = method
        for item in req:
            mc = re.search("(.+): (.+)", item)
            if not mc: continue
            key = mc.group(1)
            val = mc.group(2)
            environ[key] = val
        return environ

    def handle_request(self):
        req = self.__read_socket()
        self.__parse_request(req)

    def server_forever(self):
        while True:
            self.handle_request()

def app(environ, start_response):
    pass

if __name__ == '__main__':
    bs = BassoonServer()
    bs.server_forever()



