from contextlib import contextmanager
from typing import Dict

import pytest_asyncio

from aiohttp import ClientSession
from src.dota2api.endpoints import GET_MATCH_URL, GET_MATCHES_URL
from src.dota2api.types import AccountId, MatchId


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
    def __init__(self, body, status: int = 200, match_id: MatchId = None) -> None:
        self._status = status
        self._body = body
        self._match_id = match_id

    @contextmanager
    def mock(self, m):
        if not isinstance(self._body, list):
            m.get(
                GET_MATCH_URL.format(match_id=self._match_id),
                payload=self._body,
                status=self._status,
            )
        else:
            for match in self._body:
                match_id = match["match_id"]

                m.get(
                    GET_MATCH_URL.format(match_id=match_id),
                    payload=match,
                    status=self._status,
                )
        yield


class MockRecentMatches:
    def __init__(
        self, account_id: AccountId, body, status: int = 200, limit: int = 10
    ) -> None:
        self._body = body
        self._status = status
        self._account_id = account_id
        self._limit = limit

    @contextmanager
    def mock(self, m):
        m.get(
            f"{GET_MATCHES_URL.format(account_id=self._account_id)}?limit={self._limit}",
            payload=self._body,
            status=self._status,
        )
        yield
