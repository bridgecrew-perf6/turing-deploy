# coding: utf-8

from .controllers.handlers import (site, user, example, auth)
import tornado.web

routers = [
    tornado.web.url(r"/", site.CommunityHandler, name="index"),

    tornado.web.url(r"/customer", example.CustomerHandler, name="customer"),
    tornado.web.url(r"/admin", example.AdminHandler, name="admin"),

    tornado.web.url(r"/auth/login", auth.LoginHandler, name="auth_login"),
    tornado.web.url(r"/auth/refresh", auth.RefreshHandler, name="auth_refresh"),

    tornado.web.url(r"/user/create", user.CreateHandler, name="user_create"),
    tornado.web.url(r"/user/forbidden", user.ForbiddenHandler, name="user_forbidden"),
    tornado.web.url(r"/user/recovery", user.RecoveryHandler, name="user_recovery"),
    tornado.web.url(r"/user/kick", user.KickHandler, name="user_kick"),
    tornado.web.url(r"/user/change_password", user.ChangePasswordHandler, name="user_change_password"),

    tornado.web.url(r".*", site.PageNotFoundHandler),
]
