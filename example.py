#!/usr/bin/env python
#-*- coding: utf-8 -*-

from Bassoon import app, get, post
from Bassoon import BassoonServer

@get('/')
def index():
    return "hello world"

def main():
    host = "0.0.0.0"
    port = "8888"

    bs = BassoonServer(host=host, port=port, app=app)
    bs.serve_forever()

if __name__ == "__main__":
    main()



