import requests
import json
from typing import Any, Dict, cast


class DataClient:
    def __init__(self) -> None:
        self.symbol = "btcusd"
        self.limit = 100

    def _query_api(self) -> list[Dict[str, Any]]:
        url = f"https://api.gemini.com/v1/trades/{self.symbol}"
        params = {
            "symbol": self.symbol,
            "limit": str(self.limit),
        }
        response = requests.get(url, params=params)

        return cast(list[Dict[str, Any]], response.json())

    def _parse_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        fields = ["type", "amount", "timestampms", "price"]
        return {key: message[key] for key in fields if key in message}

    def get_data(self) -> list[Dict[str, Any]]:
        response = self._query_api()
        return [self._parse_message(trade) for trade in response]
