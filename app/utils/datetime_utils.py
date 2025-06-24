from datetime import datetime, timezone
from typing import Optional

def now_utc() -> datetime:
    """Get current datetime in UTC timezone."""
    return datetime.now(timezone.utc)

def parse_iso8601(date_str: str) -> datetime:
    """Parse ISO 8601 formatted string to timezone-aware datetime.
    
    Args:
        date_str: ISO 8601 formatted string (e.g., '2025-06-23T21:40:51Z' or '2025-06-23T17:40:51-04:00')
        
    Returns:
        timezone-aware datetime object in UTC
    """
    if not date_str:
        return None
        
    # Handle 'Z' timezone indicator
    if date_str.endswith('Z'):
        date_str = date_str[:-1] + '+00:00'
    
    # Parse the datetime
    dt = datetime.fromisoformat(date_str)
    
    # Make timezone-aware if not already
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    # Convert to UTC
    return dt.astimezone(timezone.utc)

def format_iso8601(dt: Optional[datetime]) -> Optional[str]:
    """Format datetime to ISO 8601 string in UTC.
    
    Args:
        dt: datetime object (naive or timezone-aware)
        
    Returns:
        ISO 8601 formatted string in UTC (e.g., '2025-06-23T21:40:51Z')
    """
    if dt is None:
        return None
        
    # Make timezone-aware if not already
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    # Convert to UTC and format
    return dt.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
