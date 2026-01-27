from flask import Flask
from datetime import datetime
import os


def create_app(config_name='development'):
    """
    Application factory

    Args:
        config_name: Configuration environment ('development', 'production', 'testing')

    Returns:
        Configured Flask application
    """
    # Create Flask instance with correct paths
    app = Flask(
        __name__,
        template_folder='presentation/templates',
        static_folder='presentation/static'
    )

    # Load configuration
    from app.config import config
    app.config.from_object(config[config_name])

    # Load environment variables if .env exists
    from dotenv import load_dotenv
    load_dotenv()

    # Override with environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', app.config['SECRET_KEY'])
    app.config['WEBINAR_DATE_TEXT'] = os.getenv('WEBINAR_DATE_TEXT', app.config.get('WEBINAR_DATE_TEXT', 'TBA'))

    # Register blueprints
    from app.presentation.routes.main_routes import main
    from app.presentation.routes.admin_routes import admin
    app.register_blueprint(main)
    app.register_blueprint(admin)

    # Register error handlers
    @app.errorhandler(404)
    def not_found(error):
        return "Page not found", 404

    @app.errorhandler(500)
    def internal_error(error):
        return "Internal server error", 500

    # Context processors (global template variables)
    @app.context_processor
    def inject_globals():
        """Inject global template variables"""
        return {
            'current_year': datetime.now().year
        }

    return app
