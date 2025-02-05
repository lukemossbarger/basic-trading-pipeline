class DataClient:
    def __init__(self) -> None:
        raise NotImplementedError

    def _query_api(self) -> None:
        raise NotImplementedError

    def _parse_message(self, message) -> None:
        raise NotImplementedError

    def get_data(self) -> None:
        raise NotImplementedError
