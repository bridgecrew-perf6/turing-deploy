# coding: utf-8


import tornado.web

from ._base import BaseHandler


class CommunityHandler(BaseHandler):
    def get(self):
        self.write("welcome to turing!")


class PageNotFoundHandler(BaseHandler):
    def get(self):
        self.write("404 Not Found")


class PageErrorHandler(BaseHandler):
    def get(self):
        self.write("502 Page Error")


class OtherPageErrorHandler(BaseHandler):
    def get(self):
        raise tornado.web.HTTPError(302)

