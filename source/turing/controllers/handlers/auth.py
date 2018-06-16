# coding: utf-8

import datetime
import time

from .jwtauth import jwtauth
from ...models import User

from ._base import BaseHandler


class LoginHandler(BaseHandler):
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")

        now = int(time.time())

        try:
            user = self.db.query(User).filter(User.username == username,
                                              User.passwd == self.encrypt(password),
                                              User.forbidden==False).first()

            if user:
                # 更新登录时间和token生成时间
                try:
                    user.active = now
                    user.token_time = now
                    self.db.commit()
                except Exception as e:
                    self.db.rollback()
                    self.log.error(e)

                # successful login

                payload = {
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=self.jwt_exp),
                    'iat': datetime.datetime.utcnow(),
                    'iss': 'ken',
                    'data': {
                        'username': username,
                        'token_time': now
                    }
                }

                token = self.payload_to_token(payload)
                self.write({'token': token})
            else:
                self.send_result_json(result=False, code=1, message="用户名或密码错误")

        except Exception as e:
            self.log.error(e)
            self.send_result_json(result=False, code=1, message="用户名或密码错误")


#在toke有效期内，根据旧token换取新token
@jwtauth
class RefreshHandler(BaseHandler):
    def get(self):
        now = int(time.time())
        user = self.get_current_user()
        if user:
            # 更新token生成时间
            try:
                user.token_time = now
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                self.log.error(e)
        else:
            self.send_result_json(result=False, code=1, message="token已失效")

        payload = self.token_to_payload()
        payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=self.jwt_exp)
        payload['data']['token_time'] = now
        token = self.payload_to_token(payload)
        self.write({'token': token})

