import asyncio
from .deep_client_options import DeepClientOptions

class DeepClient:
    def __init__(self, options: DeepClientOptions):
        self.gql_client = options.gql_client
        self.client = self.gql_client if self.gql_client else None

    async def select(self):
        raise NotImplementedError("Method not implemented")

    async def insert(self):
        raise NotImplementedError("Method not implemented")

    async def update(self):
        raise NotImplementedError("Method not implemented")

    async def delete(self):
        raise NotImplementedError("Method not implemented")

    async def serial(self):
        raise NotImplementedError("Method not implemented")

    async def reserve(self):
        raise NotImplementedError("Method not implemented")

    async def wait_for(self):
        raise NotImplementedError("Method not implemented")

    async def id(self):
        raise NotImplementedError("Method not implemented")

    def id_local(self):
        raise NotImplementedError("Method not implemented")

    async def guest(self):
        raise NotImplementedError("Method not implemented")

    async def jwt(self):
        raise NotImplementedError("Method not implemented")

    async def whoami(self):
        raise NotImplementedError("Method not implemented")

    async def login(self):
        raise NotImplementedError("Method not implemented")

    async def logout(self):
        raise NotImplementedError("Method not implemented")

    async def can(self):
        raise NotImplementedError("Method not implemented")

    async def name(self):
        raise NotImplementedError("Method not implemented")

    def name_local(self):
        raise NotImplementedError("Method not implemented")
