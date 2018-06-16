# coding: utf-8


def admin_permission(handler_class):
    NOT_ADMIN = "Not Admin"

    """
        Tornado JWT Auth Decorator
    """
    def wrap_execute(handler_execute):
        def require_auth(handler, kwargs):
            if handler.is_admin:
                pass
            else:
                handler._transforms = []
                handler.write(NOT_ADMIN)
                handler.finish()

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


def customer_permission(handler_class):
    NOT_CUSTOMER = "Not Customer"

    """
        Tornado JWT Auth Decorator
    """
    def wrap_execute(handler_execute):
        def require_auth(handler, kwargs):
            if not handler.is_customer:
                handler._transforms = []
                handler.write(NOT_CUSTOMER)
                handler.finish()

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
