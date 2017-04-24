# -*- coding: utf-8 -*-

"""
start wzc server
"""
from __future__ import print_function
import BaseHTTPServer
from wzc.server.server import RequestHandler
from wzc.wzc.settings import SERVER_PORT

__author__ = 'laixintao'


def server():
    """Start server"""
    print('Server start on 127.0.0.1:{}'.format(SERVER_PORT))
    server_address = ('', SERVER_PORT)
    wzc_server = BaseHTTPServer.HTTPServer(server_address, RequestHandler)
    wzc_server.serve_forever()


if __name__ == '__main__':
    server()
