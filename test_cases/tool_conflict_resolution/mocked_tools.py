"""Mocked tools for tool conflict resolution test case."""
import json
from pathlib import Path
from typing import Dict, List, Union
from datetime import datetime, timedelta
from pydantic import BaseModel


class PriceData(BaseModel):
    source: str
    product_id: str
    price: float
    currency: str
    last_updated: str
    confidence: float


class ComparisonResult(BaseModel):
    value1: Union[float, str]
    value2: Union[float, str]
    is_conflict: bool
    difference: Union[float, None]


class AuthorityInfo(BaseModel):
    authority_score: float
    is_authoritative: bool
    reason: str


def load_input_data():
    """Load input data from the local input_data.json file."""
    path = Path(__file__).parent / "input_data.json"
    with open(path) as f:
        return json.load(f)


def query_pricing_api(product_id: str) -> PriceData:
    """Retrieves current market pricing data from the live Pricing API service."""
    return PriceData(
        source="pricing_api",
        product_id=product_id,
        price=999.0,
        currency="INR",
        last_updated=(datetime.now() - timedelta(hours=2)).isoformat(),
        confidence=0.95,
    )


def query_catalog_database(product_id: str) -> PriceData:
    """Queries the centralized enterprise catalog database for stored product price records."""
    return PriceData(
        source="catalog_db",
        product_id=product_id,
        price=1099.0,
        currency="INR",
        last_updated=(datetime.now() - timedelta(days=1)).isoformat(),
        confidence=0.85,
    )


def query_cache(product_id: str) -> PriceData:
    """Checks the high-speed local cache for the most recently stored price information."""
    return PriceData(
        source="cache",
        product_id=product_id,
        price=999.0,
        currency="INR",
        last_updated=(datetime.now() - timedelta(minutes=30)).isoformat(),
        confidence=0.90,
    )


def compare_values(
    value1: Union[float, str], value2: Union[float, str]
) -> ComparisonResult:
    """Performs a statistical comparison between two data values to detect significant discrepancies."""
    v1 = float(value1)
    v2 = float(value2)
    is_conflict = v1 != v2

    return ComparisonResult(
        value1=v1,
        value2=v2,
        is_conflict=is_conflict,
        difference=abs(v1 - v2) if is_conflict else 0.0,
    )


def get_source_authority(source_name: str) -> AuthorityInfo:
    """Retrieves the authoritative trust score and system-of-record status for a specified data source."""
    authority_levels = {
        "pricing_api": AuthorityInfo(
            authority_score=0.95,
            is_authoritative=True,
            reason="Primary real-time pricing system of record.",
        ),
        "catalog_db": AuthorityInfo(
            authority_score=0.80,
            is_authoritative=False,
            reason="Secondary catalog system; may experience synchronization delays.",
        ),
        "cache": AuthorityInfo(
            authority_score=0.60,
            is_authoritative=False,
            reason="Ephemeral cache layer with potential for stale data.",
        ),
    }

    return authority_levels.get(
        source_name,
        AuthorityInfo(
            authority_score=0.5,
            is_authoritative=False,
            reason="Unknown external data source.",
        ),
    )


def get_tools() -> List[Dict[str, Union[str, callable]]]:
    """Get the tool definitions for the agent."""
    return [
        {
            "name": "query_pricing_api",
            "description": "Retrieves the current market price for a product from the authoritative Pricing API.",
            "function": query_pricing_api,
        },
        {
            "name": "query_catalog_database",
            "description": "Retrieves price records from the master catalog database.",
            "function": query_catalog_database,
        },
        {
            "name": "query_cache",
            "description": "Retrieves the latest cached price from the local performance layer.",
            "function": query_cache,
        },
        {
            "name": "compare_values",
            "description": "Detects and analyzes conflicts between two pricing data points.",
            "function": compare_values,
        },
        {
            "name": "get_source_authority",
            "description": "Evaluates the trust level and authoritative status of a specific pricing system.",
            "function": get_source_authority,
        },
    ]
