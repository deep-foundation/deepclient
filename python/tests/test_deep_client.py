import unittest
import asyncio
from deep_client import DeepClient, DeepClientOptions

class TestDeepClient(unittest.TestCase):

    def setUp(self):
        self.options = DeepClientOptions()
        self.client = DeepClient(self.options)

    def test_initialization(self):
        self.assertIsNotNone(self.client)
        self.assertIsNone(self.client.client)

    def test_methods_raise_not_implemented(self):
        async_methods = [
            'select', 'insert', 'update', 'delete', 'serial', 'reserve', 'wait_for',
            'id', 'guest', 'jwt', 'whoami', 'login', 'logout', 'can', 'name'
        ]
        sync_methods = [
            'id_local', 'name_local'
        ]

        async def test_async_methods():
            for method_name in async_methods:
                method = getattr(self.client, method_name)
                with self.assertRaises(NotImplementedError):
                    await method()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(test_async_methods())

        for method_name in sync_methods:
            method = getattr(self.client, method_name)
            with self.assertRaises(NotImplementedError):
                method()

if __name__ == '__main__':
    unittest.main()
