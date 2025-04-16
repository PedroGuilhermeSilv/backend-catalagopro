import hashlib
import json
import time
from typing import Any, Dict

import requests

from src.core.externals.shopee.connection import Connection


class ShopeeBaseAuth:
    def __init__(self, connection: Connection):
        self.connection = connection
        self.base_url = 'https://open-api.affiliate.shopee.com.br/graphql'

    def _generate_signature(self, timestamp: int, payload: str) -> str:
        """Generate SHA256 signature for API authentication."""
        factor = f"{self.connection.app_id}{timestamp}{payload}{self.connection.secret}"
        return hashlib.sha256(factor.encode()).hexdigest()

    def _make_request(self, query: str) -> Dict[str, Any]:
        """Make a request to the Shopee API."""
        timestamp = int(time.time())
        payload = json.dumps({"query": query})
        signature = self._generate_signature(timestamp, payload)
        
        headers = {
            'Authorization': f"SHA256 Credential={self.connection.app_id}, Timestamp={timestamp}, Signature={signature}",
            'Content-Type': 'application/json'
        }
        
        response = requests.post(self.base_url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json() 