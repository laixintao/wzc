# -*- coding: utf-8 -*-
import BaseHTTPServer
from wzc.storage import page_table


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    '''处理请求并返回页面'''

    def do_GET(self):
        self.page = self.create_page()
        self.send_content()

    def create_page(self):
        page_info = page_table.find_one({'path': self.path})
        return page_info['content'].encode('utf-8')

    def send_content(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(self.page)))
        self.end_headers()
        self.wfile.write(self.page)


if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = BaseHTTPServer.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
