# -*- coding: utf-8 -*-
# pylint: disable
"""
wzc_server
"""
import BaseHTTPServer
from wzc.storage import page_table
from wzc.wzc.settings import HTML_PATH, IGNORE_PATH, BASE_URL
from wzc.schedule.tasks import update


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    '''处理请求并返回页面'''

    def do_GET(self):
        """handle get method"""
        if self.path in IGNORE_PATH:
            return
        self.page = self.create_page()
        self.send_content()

    def do_POST(self):
        """ don't support POST method"""
        pass

    def create_page(self):
        """get page content"""
        page_info = page_table.find_one({'path': self.path})
        if not page_info:
            update(BASE_URL + self.path)
            page_info = page_table.find_one({'path': self.path})
        if page_info:
            filename = page_info['md5']
            with open('{}{}.html'.format(HTML_PATH, filename), 'r') as html_file:
                content = html_file.read()
                self.log_message("[GET]-SUCCESS\t: {}".format(self.path))
                return content
        else:
            self.log_error("[GET]-FAIL   \t: {}Not downloaded yet!".format(self.path))
            return ""

    def send_content(self):
        """send content to browser"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(self.page)))
        self.end_headers()
        self.wfile.write(self.page)
