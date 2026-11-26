"""
Utility validators for Lead Research Agent.
"""

import re
from typing import Optional, Tuple


def validate_company_name(name: str) -> Tuple[bool, str]:
    """Validate company name."""
    if not name or len(name.strip()) < 2:
        return False, "Company name must be at least 2 characters"
    
    if len(name) > 200:
        return False, "Company name must be less than 200 characters"
    
    return True, "Valid"


def validate_website(url: str) -> Tuple[bool, str]:
    """Validate website URL format."""
    if not url:
        return True, "Valid (optional)"
    
    # Simple URL validation
    url_pattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
    
    if not re.match(url_pattern, url):
        # Try adding http:// if missing
        url_with_http = f"http://{url}"
        if re.match(url_pattern, url_with_http):
            return True, f"Valid (URL will be treated as {url_with_http})"
        return False, "Invalid URL format"
    
    return True, "Valid"


def validate_location(location: str) -> Tuple[bool, str]:
    """Validate location string."""
    if not location:
        return True, "Valid (optional)"
    
    if len(location) > 100:
        return False, "Location must be less than 100 characters"
    
    return True, "Valid"


def validate_industry(industry: str) -> Tuple[bool, str]:
    """Validate industry string."""
    if not industry:
        return True, "Valid (optional)"
    
    if len(industry) > 100:
        return False, "Industry must be less than 100 characters"
    
    return True, "Valid"


def extract_domain_from_url(url: str) -> Optional[str]:
    """Extract domain from URL."""
    if not url:
        return None
    
    # Remove http:// or https://
    url = url.replace("https://", "").replace("http://", "")
    
    # Remove www.
    url = url.replace("www.", "")
    
    # Get domain only
    domain = url.split('/')[0].split('?')[0]
    
    return domain if domain else None
