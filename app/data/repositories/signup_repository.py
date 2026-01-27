from typing import List, Optional
from app.data.models.signup import SignupData


class SignupRepository:
    """
    Repository for signup data access
    Currently uses no backend storage (localStorage is frontend-only)
    Future: Implement with SQLAlchemy/database
    """

    def __init__(self):
        """Initialize repository"""
        # TODO: Initialize database connection when needed
        pass

    def save(self, signup: SignupData) -> bool:
        """
        Save signup data

        Current: No-op (localStorage handles storage in frontend)
        Future: Insert into database

        Args:
            signup: SignupData instance

        Returns:
            True if successful
        """
        # TODO: Implement database insert
        # Example:
        # db.session.add(signup)
        # db.session.commit()

        # For now, just validate the data
        try:
            signup.to_dict()  # Validate serialization
            return True
        except Exception:
            return False

    def get_all(self) -> List[SignupData]:
        """
        Get all signups

        Current: Returns empty list
        Future: Query database
        """
        # TODO: Implement database query
        # return [SignupData.from_dict(row) for row in db.query(...)]
        return []

    def get_by_email(self, email: str) -> Optional[SignupData]:
        """
        Find signup by email

        Current: Returns None
        Future: Query database
        """
        # TODO: Implement database query
        # row = db.query(...).filter_by(email=email).first()
        # return SignupData.from_dict(row) if row else None
        return None

    def count(self) -> int:
        """
        Count total signups

        Current: Returns 0
        Future: Query database count
        """
        # TODO: Implement database count
        # return db.query(...).count()
        return 0
