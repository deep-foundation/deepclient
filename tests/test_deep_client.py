def test_select(self):
    async def test_async_methods():
        await self.client.select(1)
        self.assertEqual(self.client.table, '1')

        result = await self.client.select('users')
        self.assertEqual(result, 'SELECT * FROM users')

        result = await self.client.select('users', ['id', 'email'])
        self.assertEqual(result, 'SELECT id, email FROM users')

        result = await self.client.select('users', ['id', 'email'], where={'id': 1})
        self.assertEqual(result, 'SELECT id, email FROM users WHERE id = 1')

        result = await self.client.select('users', ['id', 'email'], where={'id': {'$gt': 1}})
        self.assertEqual(result, 'SELECT id, email FROM users WHERE id > 1')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_async_methods())