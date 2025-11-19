from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from base import BaseModel
@dataclass
class Vehicle(BaseModel):
    table_name: str = field(default='vehicles', init=False, repr=False)
    
    id: Optional[int] = None
    name: Optional[str] = None
    model: Optional[str] = None
    rent_rate: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def get_by_name(cls, name: str) -> List['Vehicle']:
        """Get vehicles by name"""
        return cls.filter(name=name)
    
    @classmethod
    def get_available(cls) -> List['Vehicle']:
        """Get vehicles not assigned to any user"""
        fields_str = ', '.join(cls._get_fields())
        query = f"""
            SELECT {fields_str}
            FROM {cls.table_name} v
            WHERE NOT EXISTS (
                SELECT 1 FROM users u WHERE u.vehicle_id = v.id
            )
            ORDER BY v.id
        """
        rows = cls._execute_query(query)
        return [cls._row_to_instance(row) for row in rows]
    
    def is_available(self) -> bool:
        """Check if vehicle is available (not assigned)"""
        if self.id is None:
            return False
        
        query = "SELECT 1 FROM users WHERE vehicle_id = %s LIMIT 1"
        rows = self._execute_query(query, (self.id,))
        return len(rows) == 0


# ============= User Model =============

@dataclass
class User(BaseModel):
    table_name: str = field(default='users', init=False, repr=False)
    
    id: Optional[int] = None
    username: Optional[str] = None
    vehicle_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Cached vehicle (not stored in DB)
    _vehicle: Optional[Vehicle] = field(default=None, init=False, repr=False)
    
    @classmethod
    def get_by_username(cls, username: str) -> Optional['User']:
        """Get user by username"""
        results = cls.filter(username=username)
        return results[0] if results else None
    
    @classmethod
    def all_with_vehicles(cls) -> List['User']:
        """Get all users with their vehicle information"""
        query = f"""
            SELECT 
                u.id, u.username, u.vehicle_id, u.created_at, u.updated_at,
                v.id, v.name, v.model, v.rent_rate, v.created_at, v.updated_at
            FROM {cls.table_name} u
            LEFT JOIN vehicles v ON u.vehicle_id = v.id
            ORDER BY u.id
        """
        
        cur = cls._get_cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        
        users = []
        user_fields = cls._get_fields()
        vehicle_fields = Vehicle._get_fields()
        
        for row in rows:
            user_data = dict(zip(user_fields, row[:5]))
            user = cls(**user_data)
            
            # Attach vehicle if exists
            if row[5] is not None:
                vehicle_data = dict(zip(vehicle_fields, row[5:]))
                user._vehicle = Vehicle(**vehicle_data)
            
            users.append(user)
        
        return users
    
    def get_vehicle(self) -> Optional[Vehicle]:
        """Get the vehicle assigned to this user (lazy loaded)"""
        if self._vehicle is None and self.vehicle_id is not None:
            self._vehicle = Vehicle.get(self.vehicle_id)
        return self._vehicle
    
    def assign_vehicle(self, vehicle_id: int) -> 'User':
        """Assign a vehicle to this user"""
        self.vehicle_id = vehicle_id
        self._vehicle = None  # Clear cache
        return self.save()
    
    def remove_vehicle(self) -> 'User':
        """Remove vehicle assignment from this user"""
        self.vehicle_id = None
        self._vehicle = None
        return self.save()
    
    def to_dict(self, include_vehicle: bool = False) -> Dict[str, Any]:
        """Convert to dictionary, optionally including vehicle data"""
        data = super().to_dict()
        
        # Remove internal fields
        data.pop('_vehicle', None)
        
        if include_vehicle:
            vehicle = self.get_vehicle()
            data['vehicle'] = vehicle.to_dict() if vehicle else None
        
        return data