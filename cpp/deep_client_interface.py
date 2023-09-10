from typing import Any, Optional, Union, Dict, List
from deepclient import DeepClient, DeepClientOptions
from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
from aiohttp.client_exceptions import ClientConnectorError
import asyncio

global_deep_client = None


def make_deep_client(token, url):
    global global_deep_client

    if global_deep_client is None:
        if not token:
            raise ValueError("No token provided")
        if not url:
            raise ValueError("No url provided")

        transport = AIOHTTPTransport(url=url, headers={'Authorization': f"Bearer {token}"})
        client = Client(transport=transport, fetch_schema_from_transport=True)
        options = DeepClientOptions(gql_client=client)
        global_deep_client = DeepClient(options)

    return global_deep_client


def handle_error(error: Exception) -> str:
    if isinstance(error, ClientConnectorError):
        return "Cannot connect to host"
    return str(error)


def execute_async(func, *args, **kwargs):
    try:
        return asyncio.run(func(*args, **kwargs))
    except Exception as e:
        return handle_error(e)


def select(token, url, exp: Union[Dict, int, List[int]], options: Dict = {}) -> dict | str:
    async def _select(client, exp, options):
        return await client.select(exp, options)

    deep_client = make_deep_client(token, url)
    return execute_async(_select, deep_client, exp, options)


def insert(token: str, url: str, objects: Any, options: Dict = {}) -> dict | str:
    async def _insert(client, objects, options):
        return await client.insert(objects, options)

    deep_client = make_deep_client(token, url)
    return execute_async(_insert, deep_client, objects, options)


def update(token: str, url: str, exp: Dict, value: Dict, options: Dict = {}) -> dict | str:
    async def _update(client, exp, value, options):
        return await client.update(exp, value, options)

    deep_client = make_deep_client(token, url)
    return execute_async(_update, deep_client, exp, value, options)


def delete(token: str, url: str, exp: Union[Dict, int, List[int]], options: Dict = {}) -> dict | str:
    async def _delete(client, exp, options):
        return await client.delete(exp, options)

    deep_client = make_deep_client(token, url)
    return execute_async(_delete, deep_client, exp, options)


def serial(token: str, url: str, async_serial_params: Dict) -> dict | str:
    async def _serial(client, async_serial_params):
        return await client.serial(async_serial_params)

    deep_client = make_deep_client(token, url)
    return execute_async(_serial, deep_client, async_serial_params)


def id(token: str, url: str, start: Any, *path: Any) -> int | str:
    async def _id(client, start, *path):
        return await client.id(start, *path)

    deep_client = make_deep_client(token, url)
    return execute_async(_id, deep_client, start, *path)


async def reserve(token, url):
    return await make_deep_client(token, url).reserve()


async def wait_for(token, url):
    return await make_deep_client(token, url).wait_for()


def id_local(token, url):
    return make_deep_client(token, url).id_local()


async def guest(token, url):
    return await make_deep_client(token, url).guest()


async def jwt(token, url):
    return await make_deep_client(token, url).jwt()


async def whoami(token, url):
    return await make_deep_client(token, url).whoami()


async def login(token, url):
    return await make_deep_client(token, url).login()


async def logout(token, url):
    return await make_deep_client(token, url).logout()


async def can(token, url):
    return await make_deep_client(token, url).can()


async def name(token, url):
    return await make_deep_client(token, url).name()


def name_local(token, url):
    return make_deep_client(token, url).name_local()
