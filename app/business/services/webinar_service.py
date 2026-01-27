from typing import Tuple, Dict, Any
from app.data.models.signup import SignupData
from app.data.repositories.signup_repository import SignupRepository


class WebinarService:
    """
    Business logic for webinar operations
    """

    def __init__(self, config=None):
        """
        Initialize service

        Args:
            config: Flask config object (optional)
        """
        self.repository = SignupRepository()
        self.config = config or {}

    def validate_signup_data(self, data: dict) -> Tuple[bool, str]:
        """
        Validate signup data according to business rules

        Args:
            data: Dictionary with signup data

        Returns:
            Tuple of (is_valid: bool, error_message: str)
        """
        # Check required fields
        email = data.get('email', '').strip()
        consent = data.get('consent', False)

        if not email:
            return False, "Please enter your email."

        if not SignupData.is_valid_email(email):
            return False, "That email doesn't look quite right. Please check it."

        if not consent:
            return False, "Please tick the consent box to sign up."

        return True, ""

    def process_signup(self, data: dict) -> Dict[str, Any]:
        """
        Process a signup request

        Args:
            data: Dictionary with signup data

        Returns:
            Dictionary with success status and message
        """
        # Validate data
        is_valid, error_msg = self.validate_signup_data(data)
        if not is_valid:
            return {
                'success': False,
                'error': error_msg
            }

        # Create model
        try:
            signup = SignupData(
                email=data.get('email', '').strip(),
                consent=data.get('consent', False),
                first_name=data.get('firstName', '').strip() or None,
                last_name=data.get('lastName', '').strip() or None
            )
        except ValueError as e:
            return {
                'success': False,
                'error': str(e)
            }

        # Save (currently no-op)
        success = self.repository.save(signup)

        if success:
            return {
                'success': True,
                'message': "You're signed up! We'll email you webinar updates and a reminder."
            }
        else:
            return {
                'success': False,
                'error': "Something went wrong. Please try again."
            }

    def get_webinar_config(self) -> Dict[str, Any]:
        """
        Get webinar configuration/metadata

        Returns:
            Dictionary with webinar info
        """
        return {
            'date': self.config.get('WEBINAR_DATE_TEXT', 'TBA'),
            'duration': '45 min',
            'format': 'Online',
            'title': 'Get webinar updates in your inbox.'
        }
