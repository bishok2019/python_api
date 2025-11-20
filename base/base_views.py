from python_api_backend.db import get_db_connection


class BaseView:
    """Base class for all views"""

    def __init__(self, db_connection=None):
        """Initialize with optional database connection function"""
        self.get_connection = db_connection or get_db_connection


class BaseListApiView(BaseView):
    pass


class BaseRetrieveApiView(BaseView):
    pass


class BaseUpdateApiView(BaseView):
    pass


class BaseCreateApiView(BaseView):
    pass
