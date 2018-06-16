# coding: utf-8

from .jwtauth import jwtauth
from .permission import admin_permission

from ...models import User
from ...models.role_code import RoleCode

from ._base import BaseHandler
import time


#新建用户
@jwtauth
@admin_permission
class CreateHandler(BaseHandler):
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")

        try:
            user = User(username=username, passwd=self.encrypt(password), role=RoleCode.CONSUMER)
            self.db.add(user)
            self.db.commit()
            self.send_result_json(result=True, code=0, message="创建用户成功")
        except Exception as e:
            self.db.rollback()
            self.log.error(e)
            self.send_result_json(result=False, code=1, message="创建用户失败")


#封禁用户
@jwtauth
@admin_permission
class ForbiddenHandler(BaseHandler):
    def post(self):
        username = self.get_argument("username")
        print("username", username)
        try:
            user = self.db.query(User).filter(User.username == username,
                                              User.forbidden == False).first()

            if user:
                try:
                    user.forbidden = True
                    self.db.commit()
                    self.send_result_json(result=True, code=0, message="禁用用户成功")
                except Exception as e:
                    self.db.rollback()
                    self.log.error(e)
                    self.send_result_json(result=False, code=1, message="禁用用户失败")
            else:
                self.send_result_json(result=False, code=1, message="禁用用户失败")

        except Exception as e:
            self.log.error(e)
            self.send_result_json(result=False, code=1, message="禁用用户失败")


#解除封禁
@jwtauth
@admin_permission
class RecoveryHandler(BaseHandler):
    def post(self):
        username = self.get_argument("username")
        try:
            user = self.db.query(User).filter(User.username == username,
                                              User.forbidden == True).first()

            if user:
                try:
                    user.forbidden = False
                    self.db.commit()
                    self.send_result_json(result=True, code=0, message="恢复用户成功")
                except Exception as e:
                    self.db.rollback()
                    self.log.error(e)
                    self.send_result_json(result=False, code=1, message="恢复用户失败")
            else:
                self.send_result_json(result=False, code=1, message="恢复用户失败")

        except Exception as e:
            self.log.error(e)
            self.send_result_json(result=False, code=1, message="恢复用户失败")


#踢掉在线用户，强制其重新登陆
@jwtauth
@admin_permission
class KickHandler(BaseHandler):
    def post(self):
        username = self.get_argument("username")
        now = int(time.time())

        try:
            user = self.db.query(User).filter(User.username == username,
                                              User.forbidden == False).first()

            if user:
                try:
                    user.token_time = now
                    self.db.commit()
                    self.send_result_json(result=True, code=0, message="踢出用户成功")
                except Exception as e:
                    self.db.rollback()
                    self.log.error(e)
                    self.send_result_json(result=False, code=1, message="踢出用户失败")
            else:
                self.send_result_json(result=False, code=1, message="踢出用户失败")

        except Exception as e:
            self.log.error(e)
            self.send_result_json(result=False, code=1, message="踢出用户失败")


#修改用户密码
@jwtauth
@admin_permission
class ChangePasswordHandler(BaseHandler):
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")

        now = int(time.time())

        try:
            user = self.db.query(User).filter(User.username == username,
                                              User.forbidden == False).first()

            if user:
                try:
                    user.passwd = self.encrypt(password)
                    user.token_time = now
                    self.db.commit()
                    self.send_result_json(result=True, code=0, message="修改密码成功")
                except Exception as e:
                    self.db.rollback()
                    self.log.error(e)
                    self.send_result_json(result=False, code=1, message="修改密码失败")
            else:
                self.send_result_json(result=False, code=1, message="修改密码失败")

        except Exception as e:
            self.log.error(e)
            self.send_result_json(result=False, code=1, message="修改密码失败")

