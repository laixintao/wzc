# -*- coding: utf-8 -*-

"""This is a simple web server.
"""

from server import RequestHandler
import BaseHTTPServer
from wzc.wzc.settings import SERVER_PORT

__author__ = 'laixintao'


def server():
    print('Server start on 127.0.0.1:{}'.format(SERVER_PORT))
    serverAddress = ('', SERVER_PORT)
    server = BaseHTTPServer.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    server()
