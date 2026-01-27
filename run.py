#!/usr/bin/env python3
"""
Application entry point
Run with: python run.py
"""
import os
from app import create_app

# Get environment from environment variable
config_name = os.getenv('FLASK_ENV', 'development')

# Create app instance
app = create_app(config_name)

if __name__ == '__main__':
    # Get configuration
    debug = app.config.get('DEBUG', False)
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))

    # Run application
    app.run(debug=debug, host=host, port=port)
