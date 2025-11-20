"""URL routing configuration"""

import re

from core.views import (
    UserCreateApiView,
    UserListApiView,
    UserRetrieveApiView,
    UserUpdateApiView,
    VehicleCreateApiView,
    VehicleListApiView,
    VehicleRetrieveApiView,
    VehicleUpdateApiView,
)

# URL patterns mapping
urlpatterns = [
    # Vehicle URLs
    (r"^/api/vehicles/?$", VehicleListApiView),  # GET - list vehicles
    (r"^/api/vehicles/create/?$", VehicleCreateApiView),  # POST - create vehicle
    (
        r"^/api/vehicles/(\d+)/?$",
        VehicleRetrieveApiView,
    ),  # GET - retrieve single vehicle
    (r"^/api/vehicles/(\d+)/update/?$", VehicleUpdateApiView),  # PUT - update vehicle
    # User URLs
    (r"^/api/users/?$", UserListApiView),  # GET - list users
    (r"^/api/users/create/?$", UserCreateApiView),  # POST - create user
    (r"^/api/users/(\d+)/?$", UserRetrieveApiView),  # GET - retrieve single user
    (r"^/api/users/(\d+)/update/?$", UserUpdateApiView),  # PUT - update user
]


class URLRouter:
    """Router to match URLs to view classes"""

    def __init__(self):
        self.urlpatterns = urlpatterns

    def resolve(self, path):
        """Match path to a view class and extract parameters"""
        for pattern, view_class in self.urlpatterns:
            match = re.match(pattern, path)
            if match:
                return view_class, match.groups()
        return None, None
