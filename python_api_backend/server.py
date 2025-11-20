import json
import os
import sys
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer

from python_api_backend.urls import URLRouter

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class APIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the API"""

    router = URLRouter()

    def _dispatch(self, method):
        """Dispatch request to appropriate view method"""
        try:
            # Read request body if present
            content_length = int(self.headers.get("Content-Length", 0))
            body_str = (
                self.rfile.read(content_length).decode("utf-8")
                if content_length
                else None
            )
            body = json.loads(body_str) if body_str else None

            # Prepare request object
            request = {
                "method": method,
                "path": self.path,
                "headers": dict(self.headers),
                "body": body,
            }

            # Resolve URL to view class
            view_class, params = self.router.resolve(self.path)

            if view_class is None:
                self._send_response(404, {"error": "Not found"})
                return

            # Instantiate view and call method
            view = view_class()
            method_name = method.lower()

            if not hasattr(view, method_name):
                self._send_response(405, {"error": f"Method {method} not allowed"})
                return

            handler = getattr(view, method_name)

            # Call handler with request and any URL parameters
            if params:
                # Convert string params to integers if they're numeric
                params = tuple(int(p) if p.isdigit() else p for p in params)
                status_code, response_data = handler(request, *params)
            else:
                status_code, response_data = handler(request)

            self._send_response(status_code, response_data)

        except json.JSONDecodeError:
            self._send_response(400, {"error": "Invalid JSON"})
        except Exception as e:
            print("Error", str(e))
            traceback.print_exc()
            self._send_response(500, {"error": str(e)})

    def do_GET(self):
        """Handle GET requests"""
        self._dispatch("GET")

    def do_POST(self):
        """Handle POST requests"""
        self._dispatch("POST")

    def do_PUT(self):
        """Handle PUT requests"""
        self._dispatch("PUT")

    def do_DELETE(self):
        """Handle DELETE requests"""
        self._dispatch("DELETE")

    def _send_response(self, status_code, data):
        """Send JSON response"""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def log_message(self, format, *args):
        """Custom logging"""
        print(f"{self.address_string()} - {format % args}")


def run_server(host="localhost", port=8000):
    """Start the HTTP server"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, APIHandler)
    print(f"Server running on http://{host}:{port}")
    print("\nAvailable endpoints:")
    print("  GET    /api/vehicles       - List all vehicles")
    print("  POST   /api/vehicles       - Create vehicle")
    print("  GET    /api/vehicles/{id}  - Get vehicle")
    print("  PUT    /api/vehicles/{id}  - Update vehicle")
    print("  DELETE /api/vehicles/{id}  - Delete vehicle")
    print("  GET    /api/users          - List all users")
    print("  POST   /api/users          - Create user")
    print("  GET    /api/users/{id}     - Get user")
    print("  PUT    /api/users/{id}     - Update user")
    print("  DELETE /api/users/{id}     - Delete user")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
