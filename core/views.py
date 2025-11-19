from python_api_backend.db import get_db_connection
from core.serializers import VehicleSerializer, UserSerializer
from core.models import Vehicle, User
import json


class BaseView:
    """Base class for all views"""
    
    def __init__(self, db_connection=None):
        """Initialize with optional database connection function"""
        self.get_connection = db_connection or get_db_connection


class VehicleListView(BaseView):
    """Handle list and create operations for vehicles"""
    
    def get(self, request):
        """GET /api/vehicles - List all vehicles"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles")
        rows = cursor.fetchall()
        conn.close()
        
        vehicles = [Vehicle.from_db_row(row) for row in rows]
        return 200, [v.to_dict() for v in vehicles]
    
    def post(self, request):
        """POST /api/vehicles - Create a new vehicle"""
        data = VehicleSerializer.deserialize(request['body'])
        
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO vehicles (name, model, rent_rate) VALUES (?, ?, ?)",
            (data.get('name'), data.get('model'), data.get('rent_rate'))
        )
        conn.commit()
        vehicle_id = cursor.lastrowid
        conn.close()
        
        return 201, {'id': vehicle_id, 'message': 'Vehicle created'}


class VehicleDetailView(BaseView):
    """Handle retrieve, update and delete operations for a single vehicle"""
    
    def get(self, request, vehicle_id):
        """GET /api/vehicles/{id} - Retrieve a vehicle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            vehicle = Vehicle.from_db_row(row)
            return 200, vehicle.to_dict()
        return 404, {'error': 'Vehicle not found'}
    
    def put(self, request, vehicle_id):
        """PUT /api/vehicles/{id} - Update a vehicle"""
        data = VehicleSerializer.deserialize(request['body'])
        
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE vehicles SET name = ?, model = ?, rent_rate = ? WHERE id = ?",
            (data.get('name'), data.get('model'), data.get('rent_rate'), vehicle_id)
        )
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        
        if rows_affected > 0:
            return 200, {'message': 'Vehicle updated'}
        return 404, {'error': 'Vehicle not found'}
    
    def delete(self, request, vehicle_id):
        """DELETE /api/vehicles/{id} - Delete a vehicle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vehicles WHERE id = ?", (vehicle_id,))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        
        if rows_affected > 0:
            return 200, {'message': 'Vehicle deleted'}
        return 404, {'error': 'Vehicle not found'}


class UserListView(BaseView):
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
    
    def post(self, request):
        """POST /api/users - Create a new user"""
        data = UserSerializer.deserialize(request['body'])
        
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, vehicle_id) VALUES (?, ?)",
            (data.get('username'), data.get('vehicle_id'))
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        return 201, {'id': user_id, 'message': 'User created'}


class UserDetailView(BaseView):
    """Handle retrieve, update and delete operations for a single user"""
    
    def get(self, request, user_id):
        """GET /api/users/{id} - Retrieve a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            user = User.from_db_row(row)
            return 200, user.to_dict()
        return 404, {'error': 'User not found'}
    
    def put(self, request, user_id):
        """PUT /api/users/{id} - Update a user"""
        data = UserSerializer.deserialize(request['body'])
        
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET username = ?, vehicle_id = ? WHERE id = ?",
            (data.get('username'), data.get('vehicle_id'), user_id)
        )
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        
        if rows_affected > 0:
            return 200, {'message': 'User updated'}
        return 404, {'error': 'User not found'}
    
    def delete(self, request, user_id):
        """DELETE /api/users/{id} - Delete a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        
        if rows_affected > 0:
            return 200, {'message': 'User deleted'}
        return 404, {'error': 'User not found'}