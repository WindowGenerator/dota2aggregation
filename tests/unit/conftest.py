from contextlib import asynccontextmanager
from typing import Dict, List

import pytest_asyncio

from aiohttp import ClientSession


@pytest_asyncio.fixture
async def client_session() -> ClientSession:
    async with ClientSession() as client:
        yield client


class MockResponse:
    def __init__(self, body: Dict, status: int):
        self._body = body
        self.status = status

    async def json(self):
        return self._body

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


class MockMatches:
    def __init__(self, body, status: int = 200) -> None:
        self._matches_generator = iter(body)
        self._status = status

    @asynccontextmanager
    async def mock_matches(self, *args, **kwargs) -> Dict:
        yield MockResponse(next(self._matches_generator), self._status)


class MockRecentMatches:
    def __init__(self, body, status: int = 200) -> None:
        self._body = body
        self._status = status

    @asynccontextmanager
    async def mock_recent_matches(self, *args, **kwargs) -> List:
        yield MockResponse(self._body, self._status)
