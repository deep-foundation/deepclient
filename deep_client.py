async def select(self, index: int) -> None:
    if self.variables is None:
        raise RuntimeError("Variables mapping is not initialized. Make sure to call 'connect' method first.")

    try:
        await self._send_query(
            operation_name="Select",
            query="""
                mutation Select($index: Int!) {
                    select(index: $index) {
                        index
                    }
                }
            """,
            variables={
                "index": index
            },
        )
    except Exception as e:
        raise RuntimeError(f"Error executing 'select' mutation: {e}")