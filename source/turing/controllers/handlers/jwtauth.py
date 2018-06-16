# coding: utf-8

import jwt

def jwtauth(handler_class):
    INVALID_HEADER_MESSAGE = "invalid header authorization"
    AUTHORIZTION_ERROR_CODE = 401
    MISSING_AUTHORIZATION_KEY = "Missing authorization"
    INVALID_TOKEN = "invalid token"

    def return_auth_error(handler, message):
        """
            Return authorization error
        """
        handler._transforms = []
        handler.set_status(AUTHORIZTION_ERROR_CODE)
        handler.write(message)
        handler.finish()

    def return_header_error(handler):
        """
            Returh authorization header error
        """
        return_auth_error(handler, INVALID_HEADER_MESSAGE)


    """
        Tornado JWT Auth Decorator
    """
    def wrap_execute(handler_execute):
        def require_auth(handler, kwargs):
            try:
                token = handler.get_token()
                if token:
                    try:
                        payload = jwt.decode(
                            token,
                            handler.jwt_secret,
                            options=handler.jwt_option,
                            algorithms=handler.jwt_algorithm
                        )
                        current_token_time = payload['data']['token_time']
                        existing_token_time = handler.get_token_time()
                        if current_token_time != existing_token_time:
                            return_auth_error(handler, INVALID_TOKEN)

                    except Exception as e:
                        return_auth_error(handler, str(e))

                else:
                    return_auth_error(handler, MISSING_AUTHORIZATION_KEY)

            except Exception as e:
                return_header_error(handler, str(e))

            return True

        def _execute(self, transforms, *args, **kwargs):

            try:
                require_auth(self, kwargs)
            except Exception:
                return False

            return handler_execute(self, transforms, *args, **kwargs)

        return _execute

    handler_class._execute = wrap_execute(handler_class._execute)
    return handler_class



