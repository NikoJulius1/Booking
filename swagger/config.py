from flasgger import Swagger

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # Include all routes
            "model_filter": lambda tag: True,  # Include all models
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
}

# Template for API documentation
template = {
    "info": {
        "title": "Booking Service API",
        "description": "API for managing bookings and exporting booking data.",
        "version": "1.0.0",
        "contact": {
            "name": "Your Team",
            "url": "https://yourwebsite.com",
            "email": "contact@yourwebsite.com"
        }
    },
    "host": "localhost:5003",  # Update with your service's hostname
    "basePath": "/",  # Base path for the API
    "schemes": [
        "http"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        }
    }
}

def init_swagger(app):
    """Initialize Swagger with the given Flask app"""
    return Swagger(app, config=swagger_config, template=template)