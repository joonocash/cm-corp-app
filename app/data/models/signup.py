from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import re


@dataclass
class SignupData:
    """
    Data model for webinar signup
    """
    email: str
    consent: bool
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    job_title: Optional[str] = None
    company: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate data after initialization"""
        if not self.email:
            raise ValueError("Email is required")
        if not self.is_valid_email(self.email):
            raise ValueError("Invalid email format")
        if not self.consent:
            raise ValueError("Consent is required")

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        return re.match(pattern, email) is not None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'firstName': self.first_name or '',
            'lastName': self.last_name or '',
            'jobTitle': self.job_title or '',
            'company': self.company or '',
            'email': self.email,
            'consent': self.consent,
            'ts': self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'SignupData':
        """Create instance from dictionary"""
        return cls(
            email=data.get('email', ''),
            consent=data.get('consent', False),
            first_name=data.get('firstName'),
            last_name=data.get('lastName'),
            job_title=data.get('jobTitle'),
            company=data.get('company'),
            timestamp=datetime.fromisoformat(data.get('ts', datetime.now().isoformat()))
        )

    def to_csv_row(self) -> list:
        """Convert to list for CSV serialization"""
        return [
            self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            self.first_name or '',
            self.last_name or '',
            self.job_title or '',
            self.company or '',
            self.email,
        ]
