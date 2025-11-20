from base.base_model import BaseModel


class Vehicle(BaseModel):
    """Vehicle model"""

    table_name = "vehicles"

    def __init__(
        self,
        id=None,
        name=None,
        model=None,
        rent_rate=None,
        created_at=None,
        updated_at=None,
    ):
        self.id = id
        self.name = name
        self.model = model
        self.rent_rate = rent_rate
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_db_row(cls, row):
        """Create instance from database row"""
        return cls(
            id=row[0],
            name=row[1],
            model=row[2],
            rent_rate=row[3],
            created_at=row[4],
            updated_at=row[5],
        )


class User(BaseModel):
    """User model"""

    table_name = "users"

    def __init__(
        self, id=None, username=None, vehicle_id=None, created_at=None, updated_at=None
    ):
        self.id = id
        self.username = username
        self.vehicle_id = vehicle_id
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_db_row(cls, row):
        """Create instance from database row"""
        return cls(
            id=row[0],
            username=row[1],
            vehicle_id=row[2],
            created_at=row[3],
            updated_at=row[4],
        )
