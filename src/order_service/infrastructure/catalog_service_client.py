from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

import httpx


@dataclass(kw_only=True)
class CatalogItem:
    id: UUID
    name: str
    price: Decimal
    available_qty: int
    created_at: datetime


class CatalogServiceClient:
    _base_url: str
    _api_key: str

    def __init__(self, base_url: str, api_key: str) -> None:
        self._base_url = base_url
        self._api_key = api_key

    async def get_catalog_item_by_id(self, item_id: UUID) -> CatalogItem:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._base_url}/api/catalog/items/{item_id}",
                headers={"X-API-Key": self._api_key},
            )
            response.raise_for_status()
            return CatalogItem(**response.json())
