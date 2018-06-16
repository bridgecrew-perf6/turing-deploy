# coding: utf-8

import tornado.web
from tornado.log import app_log
import jwt, hashlib
from ...models import User

from ...helpers import force_int
from ...errors import BadRequest


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)

    @property
    def db(self):
        return self.settings['db']

    @property
    def jwt_exp(self):
        return self.settings['jwt_exp']

    @property
    def jwt_option(self):
        return self.settings['jwt_option']

    @property
    def jwt_secret(self):
        return self.settings['jwt_secret']

    @property
    def jwt_algorithm(self):
        return self.settings['jwt_algorithm']

    def base_url(self):
        return self.settings.get('base_url', '/')

    @property
    def log(self):
        """I can't seem to avoid typing self.log"""
        return self.settings.get('log', app_log)

    @property
    def config(self):
        return self.settings.get('config', None)

    @property
    def version_hash(self):
        return self.settings.get('version_hash', '')


    def get_int(self, name, default=None):
        return force_int(self.get_argument(name, default), default)

    def encrypt(self, password):
        return hashlib.sha512(password.encode('utf-8')).hexdigest()

    def payload_to_token(self, payload):
        return jwt.encode(payload, self.jwt_secret, self.jwt_algorithm).decode('utf-8')

    def token_to_payload(self):
        try:
            token = self.get_token()
            if not token:
                return {}

            payload = jwt.decode(token,
                                 self.jwt_secret,
                                 options=self.jwt_option,
                                 algorithms=self.jwt_algorithm)
            return payload
        except Exception as e:
            self.log.error(e)
            return {}

    # 获取当前用户名
    def get_current_username(self):
        try:
            payload = self.token_to_payload()
            data = payload['data']
            current_username = data['username']
            return current_username
        except Exception as e:
            return "Anonymous"

    # 获取当前用户
    def get_current_user(self):
        username = self.get_current_username()
        try:
            user = self.db.query(User).filter(User.username == username).first()
            return user
        except:
            return None

    # 获取当前用户的token生成时间
    def get_token_time(self):
        username = self.get_current_username()
        try:
            user = self.db.query(User).filter(User.username == username).first()
            token_time = user.token_time
            return token_time
        except:
            return None


    # 是否被封禁
    @property
    def is_forbidden(self):
        user = self.get_current_user()
        if user:
            return user.is_forbidden
        else:
            return True

    # 是否管理员
    @property
    def is_admin(self):
        user = self.get_current_user()
        if user:
            return user.is_admin and not user.is_forbidden
        else:
            return False

    # 是否普通用户
    @property
    def is_customer(self):
        user = self.get_current_user()

        if user:
            return user.is_customer and not user.is_forbidden
        else:
            return False


    def get_token(self):
        AUTHORIZATION_HEADER = 'Authorization'
        AUTHORIZATION_METHOD = 'bearer'

        def is_valid_header(parts):
            """
                Validate the header
            """
            if parts[0].lower() != AUTHORIZATION_METHOD:
                return False
            elif len(parts) == 1:
                return False
            elif len(parts) > 2:
                return False

            return True


        auth = self.request.headers.get(AUTHORIZATION_HEADER)
        if auth:
            parts = auth.split()
            if not is_valid_header(parts):
                raise BadRequest

            token = parts[1]

            return token
        else:
            return None

    def send_result_json(self, result, code, message):
        result = {
            'result': result,
            'code': code,
            'message': message
        }
        return self.write(result)



