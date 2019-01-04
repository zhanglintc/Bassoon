#!/usr/bin/env python
#-*- coding: utf-8 -*-

import socket

class BassoonServer(object):
    __QUEUE_SIZE = 5
    __BUFF_SIZE  = 4096

    def __init__(self):
        super(BassoonServer, self).__init__()
        self.sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def server_forever(self, host="localhost", port="8888"):
        addr = (host, int(port))
        self.sckt.bind(addr)
        self.sckt.listen(self.__QUEUE_SIZE)

        while True:
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

            print req

if __name__ == '__main__':
    bs = BassoonServer()
    bs.server_forever()
