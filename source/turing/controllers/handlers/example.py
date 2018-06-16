# coding: utf-8

from .permission import admin_permission, customer_permission
from .jwtauth import jwtauth


from ._base import BaseHandler


@jwtauth
@customer_permission
class CustomerHandler(BaseHandler):
    def get(self):
        self.write("Hello, " + self.get_current_username() + "!   You are customer")


@jwtauth
@admin_permission
class AdminHandler(BaseHandler):
    def get(self):
        self.write("Hello, " + self.get_current_username() + "!   You are admin")
