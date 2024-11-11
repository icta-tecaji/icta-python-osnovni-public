"""Module for getting IP information."""

from __future__ import annotations

import time

import httpx
from db.operations import ip_metadata_operations
from loguru import logger
from pydantic import BaseModel

BASE_IP_ENDPOINT_URL = "http://ip-api.com/json"


class IpMetadata(BaseModel):
    """Model for IP metadata."""

    ip: str
    country: str | None
    country_code: str | None
    region: str | None
    region_name: str | None
    city: str | None
    zip: str | None
    lat: float | None
    lon: float | None
    isp: str | None
    organization: str | None
    autonomous_system: str | None


def get_metadata_for_ip(ip: str) -> IpMetadata | None:
    """Get metadata for a given IP address."""
    # Check if the data is already in the database
    data = ip_metadata_operations.get_data(ip)
    if data:
        logger.debug(f"Metadata for IP {ip} found in the database.")
        return IpMetadata(**data)
    # Get metadata from the API
    link = f"{BASE_IP_ENDPOINT_URL}/{ip}"
    logger.info(f"Getting metadata for IP from API: {ip}")
    with httpx.Client() as client:
        time.sleep(1)
        response = client.get(link)
        if response.status_code != httpx.codes.OK:
            logger.error(f"Failed to get metadata for IP: {ip}, status code: {response.status_code}, response: {response.text}")
            return None
        ip_metadata = response.json()
        ip_metadata["ip"] = ip_metadata.pop("query")
        ip_metadata["country_code"] = ip_metadata.pop("countryCode")
        ip_metadata["region_name"] = ip_metadata.pop("regionName")
        ip_metadata["organization"] = ip_metadata.pop("org")
        ip_metadata["autonomous_system"] = ip_metadata.pop("as")
        data = IpMetadata.model_validate(ip_metadata)

    # Save the data to the database
    ip_metadata_operations.insert_data(data.model_dump())
    return data
