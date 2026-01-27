import os
from datetime import timedelta


class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Webinar configuration
    WEBINAR_DATE_TEXT = 'TBA'

    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Future: Database configuration
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENV = 'development'
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENV = 'production'
    TESTING = False

    # Override with more secure settings
    SECRET_KEY = os.getenv('SECRET_KEY')  # Must be set in production

    # Production-only settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    ENV = 'testing'

    # Testing-specific settings
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
