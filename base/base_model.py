from dataclasses import asdict, dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

import psycopg

from python_api_backend.settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

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
                password=DB_PASSWORD,
            )
        return cls._connection

    @classmethod
    def close_connection(cls):
        if cls._connection and not cls._connection.closed:
            cls._connection.close()
            cls._connection = None


class BaseModel:
    def to_dict(self):
        # a = self.__dict__.items()
        # for k, v in a:
        #     if hasattr(v, 'isoformat'):
        #         print(f"this is isoformat{v.isoformat}")
        #         print(f"this is isoformat calling{v.isoformat()}")
        #     else:
        #         print("Not Found")
        # # # print (a)
        """Convert model instance to dictionary"""
        result = {}
        for key, value in self.__dict__.items():
            # print(f"name:{key}:{dir(value)} {hasattr(value, 'isoformat')}")

            if not key.startswith("_"):
                # Handle d atetime objects
                if hasattr(value, "isoformat"):
                    result[key] = value.isoformat()
                # Handle Decimal objects (from database)
                elif isinstance(value, Decimal):
                    result[key] = float(value)

                else:
                    result[key] = value
        return result
