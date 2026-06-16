class Service:
    def __init__(self, session, user):
        self._db = session
        self.user = user

    def _decorator(self, perm: str):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                return func(self, *args, **kwargs)

            return wrapper

        return decorator

    def check_permission(self) -> bool:
        if not self.user.is_admin:
            return True
        return False  # Permission granted
