import os
import re

def validate_path(path):
    """
    Validate file path to prevent directory traversal
    """
    # Check for common directory traversal patterns
    if re.search(r'\.\./', path) or '/.' in path:
        return False
    
    # Only allow alphanumeric characters, underscores, and hyphens
    if not re.match(r'^[\w\-\.]+$', path):
        return False
        
    return True