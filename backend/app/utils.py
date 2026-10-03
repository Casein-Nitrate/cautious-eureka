"""
Utility functions for Division 1 - Session Service.
Provides ID generation and helper functions.
"""

import secrets
import string


def generate_session_id() -> str:
    """
    Generate a unique session ID.
    
    Format: 'S' + 8 random alphanumeric characters (uppercase A-Z and digits 0-9).
    Uses cryptographically secure random number generation.
    
    Returns:
        str: Session ID in format 'SXXXXXXXX'
        
    Example:
        >>> session_id = generate_session_id()
        >>> session_id.startswith('S') and len(session_id) == 9
        True
    """
    # Use only uppercase letters and digits for clarity
    alphabet = string.ascii_uppercase + string.digits
    random_part = ''.join(secrets.choice(alphabet) for _ in range(8))
    return f'S{random_part}'


def generate_message_id() -> str:
    """
    Generate a unique message ID.
    
    Format: 'M' + 8 random alphanumeric characters (uppercase A-Z and digits 0-9).
    Uses cryptographically secure random number generation.
    
    Returns:
        str: Message ID in format 'MXXXXXXXX'
        
    Example:
        >>> message_id = generate_message_id()
        >>> message_id.startswith('M') and len(message_id) == 9
        True
    """
    alphabet = string.ascii_uppercase + string.digits
    random_part = ''.join(secrets.choice(alphabet) for _ in range(8))
    return f'M{random_part}'


def generate_escalation_id() -> str:
    """
    Generate a unique escalation ID.
    
    Format: 'ESC' + 8 random alphanumeric characters (uppercase A-Z and digits 0-9).
    Uses cryptographically secure random number generation.
    
    Returns:
        str: Escalation ID in format 'ESCXXXXXXXX'
        
    Example:
        >>> escalation_id = generate_escalation_id()
        >>> escalation_id.startswith('ESC') and len(escalation_id) == 11
        True
    """
    alphabet = string.ascii_uppercase + string.digits
    random_part = ''.join(secrets.choice(alphabet) for _ in range(8))
    return f'ESC{random_part}'


# For testing purposes
if __name__ == "__main__":
    # Generate sample IDs
    print(f"Session ID: {generate_session_id()}")
    print(f"Message ID: {generate_message_id()}")
    print(f"Escalation ID: {generate_escalation_id()}")
