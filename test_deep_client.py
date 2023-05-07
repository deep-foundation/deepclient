import asyncio
import unittest
from deepclient import DeepClient


class TestDeepClient(unittest.TestCase):

    def setUp(self):
        self.client = DeepClient(api_key="fake-api-key")

    def tearDown(self):
        pass

    def test_select(self):

        async def test_async_methods():
            await self.client.select(1)
            await self.client.select(None)
            await self.client.select({"variables": "some_variables"})
            with self.assertRaises(TypeError):
                await self.client.select({"variables": None})
        loop = asyncio.get_event_loop()
        loop.run_until_complete(test_async_methods())

if __name__ == '__main__':
    unittest.main()