"""
Mocked tools for tool conflict resolution test case.
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta


def query_pricing_api(product_id: str) -> Dict[str, Any]:
    """
    Query pricing API for product price.
    
    Args:
        product_id: Product identifier
        
    Returns:
        Price data from API
    """
    return {
        "source": "pricing_api",
        "product_id": product_id,
        "price": 999,
        "currency": "INR",
        "last_updated": (datetime.now() - timedelta(hours=2)).isoformat(),
        "confidence": 0.95
    }


def query_catalog_database(product_id: str) -> Dict[str, Any]:
    """
    Query catalog database for product price.
    
    Args:
        product_id: Product identifier
        
    Returns:
        Price data from database
    """
    return {
        "source": "catalog_db",
        "product_id": product_id,
        "price": 1099,
        "currency": "INR",
        "last_updated": (datetime.now() - timedelta(days=1)).isoformat(),
        "confidence": 0.85
    }


def query_cache(product_id: str) -> Dict[str, Any]:
    """
    Query cache for product price.
    
    Args:
        product_id: Product identifier
        
    Returns:
        Price data from cache
    """
    return {
        "source": "cache",
        "product_id": product_id,
        "price": 999,
        "currency": "INR",
        "last_updated": (datetime.now() - timedelta(minutes=30)).isoformat(),
        "confidence": 0.90
    }


def compare_values(value1: Any, value2: Any) -> Dict[str, Any]:
    """
    Compare two values for conflicts.
    
    Args:
        value1: First value
        value2: Second value
        
    Returns:
        Comparison result
    """
    is_conflict = value1 != value2
    
    return {
        "value1": value1,
        "value2": value2,
        "is_conflict": is_conflict,
        "difference": abs(value1 - value2) if isinstance(value1, (int, float)) and isinstance(value2, (int, float)) else None
    }


def get_source_authority(source_name: str) -> Dict[str, Any]:
    """
    Get authority level of a data source.
    
    Args:
        source_name: Name of the data source
        
    Returns:
        Authority information
    """
    authority_levels = {
        "pricing_api": {
            "authority_score": 0.95,
            "is_authoritative": True,
            "reason": "Primary pricing system"
        },
        "catalog_db": {
            "authority_score": 0.80,
            "is_authoritative": False,
            "reason": "Secondary catalog system"
        },
        "cache": {
            "authority_score": 0.60,
            "is_authoritative": False,
            "reason": "Cached data, may be stale"
        }
    }
    
    return authority_levels.get(source_name, {
        "authority_score": 0.5,
        "is_authoritative": False,
        "reason": "Unknown source"
    })


def get_tools() -> List[Dict[str, Any]]:
    """
    Get list of available tools for this test case.
    
    Returns:
        List of tool definitions
    """
    return [
        {
            "name": "query_pricing_api",
            "description": "Query pricing API for product price (returns ₹999)",
            "function": query_pricing_api
        },
        {
            "name": "query_catalog_database",
            "description": "Query catalog database for product price (returns ₹1099)",
            "function": query_catalog_database
        },
        {
            "name": "query_cache",
            "description": "Query cache for product price (returns ₹999)",
            "function": query_cache
        },
        {
            "name": "compare_values",
            "description": "Compare two values to detect conflicts",
            "function": compare_values
        },
        {
            "name": "get_source_authority",
            "description": "Get authority level of a data source",
            "function": get_source_authority
        }
    ]
