import psycopg
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
from python_api_backend.settings import *
# from python_api_backend.settings import DATABASE_CONFIG


class DatabaseConnection:
    """Singleton database connection manager"""
    _connection = None
    
    @classmethod
    # def get_connection(cls):
    #     if cls._connection is None or cls._connection.closed:
    #         cls._connection = psycopg.connect(
    #             host=DATABASE_CONFIG.DB_HOST,
    #             port=DATABASE_CONFIG.DB_PORT,
    #             dbname=DATABASE_CONFIG.DB_NAME,
    #             user=DATABASE_CONFIG.DB_USER,
    #             password=DATABASE_CONFIG.DB_PASSWORD
    #         )
    #     return cls._connection
    @classmethod
    def get_connection(cls):
        if cls._connection is None or cls._connection.closed:
            cls._connection = psycopg.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
        return cls._connection
    
    @classmethod
    def close_connection(cls):
        if cls._connection and not cls._connection.closed:
            cls._connection.close()
            cls._connection = None


class BaseModel:
    """
    Base model class with common CRUD operations
    All dataclass models should inherit from this
    """
    table_name: str = None  # Must be defined in child classes
    
    @classmethod
    def _get_cursor(cls):
        """Get database cursor"""
        conn = DatabaseConnection.get_connection()
        return conn.cursor()
    
    @classmethod
    def _execute_query(cls, query, params=None, fetch=True, commit=False):
        """Execute a query and optionally fetch results"""
        cur = cls._get_cursor()
        cur.execute(query, params or ())
        
        result = None
        if fetch:
            result = cur.fetchall()
        
        if commit:
            DatabaseConnection.get_connection().commit()
        
        cur.close()
        return result
    
    @classmethod
    def _get_fields(cls) -> List[str]:
        """Get field names from dataclass"""
        from dataclasses import fields
        return [f.name for f in fields(cls)]
    
    @classmethod
    def _get_insert_fields(cls) -> List[str]:
        """Get fields for INSERT (excluding auto-generated ones)"""
        return [f for f in cls._get_fields() if f not in ['id', 'created_at', 'updated_at']]
    
    @classmethod
    def _row_to_instance(cls, row, column_names=None):
        """Convert database row to model instance"""
        if row is None:
            return None
        
        if column_names is None:
            column_names = cls._get_fields()
        
        data = dict(zip(column_names, row))
        return cls(**data)
    
    # ============= CRUD Operations =============
    
    @classmethod
    def all(cls) -> List['BaseModel']:
        """Get all records"""
        fields_str = ', '.join(cls._get_fields())
        query = f"SELECT {fields_str} FROM {cls.table_name} ORDER BY id"
        rows = cls._execute_query(query)
        return [cls._row_to_instance(row) for row in rows]
    
    @classmethod
    def get(cls, pk: int) -> Optional['BaseModel']:
        """Get single record by primary key"""
        fields_str = ', '.join(cls._get_fields())
        query = f"SELECT {fields_str} FROM {cls.table_name} WHERE id = %s"
        rows = cls._execute_query(query, (pk,))
        
        if rows:
            return cls._row_to_instance(rows[0])
        return None
    
    @classmethod
    def filter(cls, **conditions) -> List['BaseModel']:
        """Filter records by conditions"""
        if not conditions:
            return cls.all()
        
        valid_fields = cls._get_fields()
        where_clauses = []
        values = []
        
        for field, value in conditions.items():
            if field in valid_fields:
                where_clauses.append(f"{field} = %s")
                values.append(value)
        
        if not where_clauses:
            return []
        
        fields_str = ', '.join(cls._get_fields())
        query = f"SELECT {fields_str} FROM {cls.table_name} WHERE {' AND '.join(where_clauses)}"
        rows = cls._execute_query(query, tuple(values))
        
        return [cls._row_to_instance(row) for row in rows]
    
    def save(self) -> 'BaseModel':
        """Insert new record or update existing one"""
        if self.id is None:
            return self._insert()
        else:
            return self._update()
    
    def _insert(self) -> 'BaseModel':
        """Insert new record"""
        insert_fields = self._get_insert_fields()
        values = [getattr(self, f) for f in insert_fields]
        
        placeholders = ', '.join(['%s'] * len(insert_fields))
        all_fields = ', '.join(self._get_fields())
        
        query = f"""
            INSERT INTO {self.table_name} ({', '.join(insert_fields)})
            VALUES ({placeholders})
            RETURNING {all_fields}
        """
        
        rows = self._execute_query(query, tuple(values), fetch=True, commit=True)
        
        if rows:
            # Update instance with returned values (including id, timestamps)
            for field, value in zip(self._get_fields(), rows[0]):
                setattr(self, field, value)
        
        return self
    
    def _update(self) -> 'BaseModel':
        """Update existing record"""
        update_fields = [f for f in self._get_insert_fields()]
        
        set_clauses = [f"{f} = %s" for f in update_fields]
        values = [getattr(self, f) for f in update_fields]
        values.append(self.id)
        
        all_fields = ', '.join(self._get_fields())
        
        query = f"""
            UPDATE {self.table_name}
            SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING {all_fields}
        """
        
        rows = self._execute_query(query, tuple(values), fetch=True, commit=True)
        
        if rows:
            for field, value in zip(self._get_fields(), rows[0]):
                setattr(self, field, value)
        
        return self
    
    def delete(self) -> bool:
        """Delete this record"""
        if self.id is None:
            return False
        
        query = f"DELETE FROM {self.table_name} WHERE id = %s"
        self._execute_query(query, (self.id,), fetch=False, commit=True)
        return True
    
    @classmethod
    def delete_by_id(cls, pk: int) -> bool:
        """Delete record by primary key"""
        query = f"DELETE FROM {cls.table_name} WHERE id = %s RETURNING id"
        rows = cls._execute_query(query, (pk,), fetch=True, commit=True)
        return bool(rows)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert instance to dictionary"""
        data = asdict(self)
        
        # Convert datetime to ISO format
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        
        return data


# ============= Vehicle Model =============

# @dataclass
# class Vehicle(BaseModel):
#     table_name: str = field(default='vehicles', init=False, repr=False)
    
#     id: Optional[int] = None
#     name: Optional[str] = None
#     model: Optional[str] = None
#     rent_rate: Optional[float] = None
#     created_at: Optional[datetime] = None
#     updated_at: Optional[datetime] = None
    
#     @classmethod
#     def get_by_name(cls, name: str) -> List['Vehicle']:
#         """Get vehicles by name"""
#         return cls.filter(name=name)
    
#     @classmethod
#     def get_available(cls) -> List['Vehicle']:
#         """Get vehicles not assigned to any user"""
#         fields_str = ', '.join(cls._get_fields())
#         query = f"""
#             SELECT {fields_str}
#             FROM {cls.table_name} v
#             WHERE NOT EXISTS (
#                 SELECT 1 FROM users u WHERE u.vehicle_id = v.id
#             )
#             ORDER BY v.id
#         """
#         rows = cls._execute_query(query)
#         return [cls._row_to_instance(row) for row in rows]
    
#     def is_available(self) -> bool:
#         """Check if vehicle is available (not assigned)"""
#         if self.id is None:
#             return False
        
#         query = "SELECT 1 FROM users WHERE vehicle_id = %s LIMIT 1"
#         rows = self._execute_query(query, (self.id,))
#         return len(rows) == 0


# # ============= User Model =============

# @dataclass
# class User(BaseModel):
#     table_name: str = field(default='users', init=False, repr=False)
    
#     id: Optional[int] = None
#     username: Optional[str] = None
#     vehicle_id: Optional[int] = None
#     created_at: Optional[datetime] = None
#     updated_at: Optional[datetime] = None
    
#     # Cached vehicle (not stored in DB)
#     _vehicle: Optional[Vehicle] = field(default=None, init=False, repr=False)
    
#     @classmethod
#     def get_by_username(cls, username: str) -> Optional['User']:
#         """Get user by username"""
#         results = cls.filter(username=username)
#         return results[0] if results else None
    
#     @classmethod
#     def all_with_vehicles(cls) -> List['User']:
#         """Get all users with their vehicle information"""
#         query = f"""
#             SELECT 
#                 u.id, u.username, u.vehicle_id, u.created_at, u.updated_at,
#                 v.id, v.name, v.model, v.rent_rate, v.created_at, v.updated_at
#             FROM {cls.table_name} u
#             LEFT JOIN vehicles v ON u.vehicle_id = v.id
#             ORDER BY u.id
#         """
        
#         cur = cls._get_cursor()
#         cur.execute(query)
#         rows = cur.fetchall()
#         cur.close()
        
#         users = []
#         user_fields = cls._get_fields()
#         vehicle_fields = Vehicle._get_fields()
        
#         for row in rows:
#             user_data = dict(zip(user_fields, row[:5]))
#             user = cls(**user_data)
            
#             # Attach vehicle if exists
#             if row[5] is not None:
#                 vehicle_data = dict(zip(vehicle_fields, row[5:]))
#                 user._vehicle = Vehicle(**vehicle_data)
            
#             users.append(user)
        
#         return users
    
#     def get_vehicle(self) -> Optional[Vehicle]:
#         """Get the vehicle assigned to this user (lazy loaded)"""
#         if self._vehicle is None and self.vehicle_id is not None:
#             self._vehicle = Vehicle.get(self.vehicle_id)
#         return self._vehicle
    
#     def assign_vehicle(self, vehicle_id: int) -> 'User':
#         """Assign a vehicle to this user"""
#         self.vehicle_id = vehicle_id
#         self._vehicle = None  # Clear cache
#         return self.save()
    
#     def remove_vehicle(self) -> 'User':
#         """Remove vehicle assignment from this user"""
#         self.vehicle_id = None
#         self._vehicle = None
#         return self.save()
    
#     def to_dict(self, include_vehicle: bool = False) -> Dict[str, Any]:
#         """Convert to dictionary, optionally including vehicle data"""
#         data = super().to_dict()
        
#         # Remove internal fields
#         data.pop('_vehicle', None)
        
#         if include_vehicle:
#             vehicle = self.get_vehicle()
#             data['vehicle'] = vehicle.to_dict() if vehicle else None
        
#         return data