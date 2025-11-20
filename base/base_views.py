from python_api_backend.db import get_db_connection


class BaseView:
    """Base class for all views"""

    def __init__(self, db_connection=None):
        """Initialize with optional database connection function"""
        self.get_connection = db_connection or get_db_connection


class BaseListApiView(BaseView):
    table_name = None  # Override in subclass
    model_class = None  # Override in subclass

    def validate_query_params(self, request):
        # Override in subclass for custom validation
        return True, None

    def get(self, request):
        if not self.table_name:
            return 400, {
                "data": None,
                "message": "Table not found.",
            }
        if not self.model_class:
            return 400, {
                "data": None,
                "message": "Model Not Found",
            }
        is_valid, error = self.validate_query_params(request)
        if not is_valid:
            return 400, {"data": None, "message": error}
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name}")
        rows = cursor.fetchall()
        conn.close()

        items = [self.model_class.from_db_row(row) for row in rows]
        return 200, {
            "data": [item.to_dict() for item in items],
            "message": f"{self.table_name.capitalize()} fetched successfully",
        }

    pass


class BaseRetrieveApiView(BaseView):
    pass


class BaseUpdateApiView(BaseView):
    pass


class BaseCreateApiView(BaseView):
    pass
