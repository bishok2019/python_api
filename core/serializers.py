from base.base_serializer import BaseSerializer

class VehicleSerializer(BaseSerializer):
    """Serializes Vehicle data between JSON and Python objects"""
    
    @staticmethod
    def deserialize(json_data):
        """Convert JSON to Python dict for database operations"""
        allowed_fields = ['name', 'model', 'rent_rate']
        return {k: v for k, v in json_data.items() if k in allowed_fields}

class UserSerializer(BaseSerializer):
    """Serializes User data between JSON and Python objects"""
    
    @staticmethod
    def deserialize(json_data):
        """Convert JSON to Python dict for database operations"""
        allowed_fields = ['username', 'vehicle_id']
        return {k: v for k, v in json_data.items() if k in allowed_fields}