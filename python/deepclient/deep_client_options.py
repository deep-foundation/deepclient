from typing import Any

class DeepClientOptions:
    def __init__(self, gql_client: Any = None):
        self.gql_client = gql_client
