from flasgger import Swagger

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',  # Internal endpoint to serve API specs
            "route": '/apispec.json',  # Route where the specs are served
            "rule_filter": lambda rule: True,  # Include all routes by default
            "model_filter": lambda tag: True,  # Include all models
        }
    ],
    "static_url_path": "/flasgger_static",  # Path for static assets (e.g., Swagger UI files)
    "swagger_ui": True,  # Enable Swagger UI
    "specs_route": "/docs"  # Route for the Swagger UI
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