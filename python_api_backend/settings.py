from decouple import config
# PostgreSQL Database configuration

# DATABASE_CONFIG = {
#     'HOST': config('DB_HOST', 'localhost'),
#     'PORT': config('DB_PORT', 5434),
#     'NAME': config('DB_NAME', 'python_api_db'),
#     'USER': config('DB_USER', 'admin'),
#     'PASSWORD': config('DB_PASSWORD', 'admin123'),
# }

# PostgreSQL Database configuration
DB_USER = config('DB_USER','admin')
DB_PASSWORD = config('DB_PASSWORD',"admin123")
DB_HOST = config('DB_HOST',"localhost")
DB_PORT = config('DB_PORT',5434)
DB_NAME = config("DB_NAME","python_api_db")

# Server configuration
HOST = 'localhost'
PORT = 8000