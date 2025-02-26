import requests
import json


class DataClient:
    def __init__(self) -> None:
        self.symbol = "btcusd"
        self.limit = 100

    def _query_api(self) -> dict:
        url = f"https://api.gemini.com/v1/trades/{self.symbol}"
        params = {
            "symbol": self.symbol,
            "limit": self.limit,
        }
        response = requests.get(url, params=params)

        return response.json()  # Return parsed JSON data from the API

    def _parse_message(self, message: str) -> None:
        fields = ["type", "amount", "timestampms", "price"]
        return {key: message[key] for key in fields if key in message}

    def get_data(self) -> None:
        response = self._query_api()
        return [self._parse_message(trade) for trade in response]
