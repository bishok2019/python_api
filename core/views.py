from base import (
    BaseCreateApiView,
    BaseListApiView,
    BaseRetrieveApiView,
    BaseUpdateApiView,
)
from core.models import User, Vehicle
from core.serializers import UserSerializer, VehicleSerializer


class VehicleListApiView(BaseListApiView):
    """Handle list operations for vehicles"""

    # def get(self, request):
    #     """GET /api/vehicles - List all vehicles"""
    #     conn = self.get_connection()
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM vehicles")
    #     rows = cursor.fetchall()
    #     conn.close()

    #     vehicles = [Vehicle.from_db_row(row) for row in rows]
    #     return 200, {
    #         "data": [v.to_dict() for v in vehicles],
    #         "message": "Vehicle fetched Successfully",
    #     }
    table_name = "vehicles"
    model_class = Vehicle


class VehicleCreateApiView(BaseCreateApiView):
    """Handle list operations for vehicles"""

    def post(self, request):
        """POST /api/vehicles - Create a new vehicle"""
        data = VehicleSerializer.deserialize(request["body"])

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO vehicles (name, model, rent_rate) VALUES (%s, %s, %s)",
            (data.get("name"), data.get("model"), data.get("rent_rate")),
        )
        conn.commit()
        vehicle_id = cursor.lastrowid
        conn.close()

        return 201, {
            "data": [
                {
                    "id": vehicle_id,
                }
            ],
            "message": "Vehicle created",
        }


class VehicleRetrieveApiView(BaseRetrieveApiView):
    """Handle retrieve, update and delete operations for a single vehicle"""

    def get(self, request, vehicle_id):
        """GET /api/vehicles/{id} - Retrieve a vehicle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            vehicle = Vehicle.from_db_row(row)
            return 200, {
                "data": [vehicle.to_dict()],
                "message": "Vehicle retrieved successfully",
            }
        return 404, {"error": "Vehicle not found"}


class VehicleUpdateApiView(BaseUpdateApiView):
    def put(self, request, vehicle_id):
        """PUT /api/vehicles/{id} - Update a vehicle"""
        data = VehicleSerializer.deserialize(request["body"])

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE vehicles SET name = %s, model = %s rent_rate = %s WHERE id = %s",
            (data.get("name"), data.get("model"), data.get("rent_rate"), vehicle_id),
        )
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()

        if rows_affected > 0:
            return 200, {"message": "Vehicle updated"}
        return 404, {"error": "Vehicle not found"}

    # def delete(self, request, vehicle_id):
    #     """DELETE /api/vehicles/{id} - Delete a vehicle"""
    #     conn = self.get_connection()
    #     cursor = conn.cursor()
    #     cursor.execute("DELETE FROM vehicles WHERE id = %s", (vehicle_id,))
    #     conn.commit()
    #     rows_affected = cursor.rowcount
    #     conn.close()

    #     if rows_affected > 0:
    #         return 200, {'message': 'Vehicle deleted'}
    #     return 404, {'error': 'Vehicle not found'}


class UserListApiView(BaseListApiView):
    """Handle list and create operations for users"""

    def get(self, request):
        """GET /api/users - List all users"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        conn.close()

        users = [User.from_db_row(row) for row in rows]
        return 200, [u.to_dict() for u in users]


class UserCreateApiView(BaseCreateApiView):
    def post(self, request):
        """POST /api/users - Create a new user"""
        data = UserSerializer.deserialize(request["body"])

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, vehicle_id) VALUES (%s, %s)",
            (data.get("username"), data.get("vehicle_id")),
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()

        return 201, {"id": user_id, "message": "User created"}


class UserRetrieveApiView(BaseRetrieveApiView):
    """Handle retrieve, update and delete operations for a single user"""

    def get(self, request, user_id):
        """GET /api/users/{id} - Retrieve a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            user = User.from_db_row(row)
            return 200, user.to_dict()
        return 404, {"error": "User not found"}


class UserUpdateApiView(BaseUpdateApiView):
    def put(self, request, user_id):
        """PUT /api/users/{id} - Update a user"""
        data = UserSerializer.deserialize(request["body"])

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET username = %s, vehicle_id = %s WHERE id = %s",
            (data.get("username"), data.get("vehicle_id"), user_id),
        )
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()

        if rows_affected > 0:
            return 200, {"message": "User updated"}
        return 404, {"error": "User not found"}

    # def delete(self, request, user_id):
    #     """DELETE /api/users/{id} - Delete a user"""
    #     conn = self.get_connection()
    #     cursor = conn.cursor()
    #     cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    #     conn.commit()
    #     rows_affected = cursor.rowcount
    #     conn.close()

    #     if rows_affected > 0:
    #         return 200, {'message': 'User deleted'}
    #     return 404, {'error': 'User not found'}
