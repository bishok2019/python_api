"""URL routing configuration"""

from core.views import (
    VehicleListView, VehicleDetailView,
    UserListView, UserDetailView
)
import re


# URL patterns mapping
urlpatterns = [
    # Vehicle URLs
    (r'^/api/vehicles/?$', VehicleListView),
    (r'^/api/vehicles/(\d+)/?$', VehicleDetailView),
    
    # User URLs
    (r'^/api/users/?$', UserListView),
    (r'^/api/users/(\d+)/?$', UserDetailView),
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