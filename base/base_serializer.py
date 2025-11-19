import json
from datetime import datetime
from typing import List

class BaseSerializer:
    def __init__(self, instance, include_fields: List[str] = None, exclude_fields: List[str] = None):
        """
        :param instance: The model instance or list of instances
        :param include_fields: Only include these fields
        :param exclude_fields: Exclude these fields
        """
        self.instance = instance
        self.include_fields = include_fields
        self.exclude_fields = exclude_fields or []

    def _serialize_instance(self, obj):
        data = {}
        for key, value in obj.__dict__.items():
            if self.include_fields and key not in self.include_fields:
                continue
            if key in self.exclude_fields:
                continue

            # Nested model
            if hasattr(value, "__dict__"):
                data[key] = self._serialize_instance(value)
            # datetime to ISO
            elif isinstance(value, datetime):
                data[key] = value.isoformat()
            else:
                data[key] = value
        return data

    def to_dict(self):
        if isinstance(self.instance, list):
            return [self._serialize_instance(obj) for obj in self.instance]
        return self._serialize_instance(self.instance)

    def to_json(self, **kwargs):
        return json.dumps(self.to_dict(), **kwargs)
