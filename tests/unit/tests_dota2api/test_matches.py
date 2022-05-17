import pytest

from aiohttp import ClientSession
from aioresponses import aioresponses
from src.dota2api.matches import get_match_info
from src.dota2api.types import Dota2ApiError
from tests.data.dota2api_data.internal_server_error import (
    MATCHES_INFO_INTERNAL_SERVER_ERROR,
)
from tests.data.dota2api_data.invalid_schema.matches_info import (
    MATCHES_INFO_1 as INVALID_MATCHES_INFO_1,
)
from tests.data.dota2api_data.invalid_schema.matches_info import (
    MATCHES_INFO_2 as INVALID_MATCHES_INFO_2,
)
from tests.data.dota2api_data.not_found_error import MATCHES_INFO_NOT_FOUND_ERROR
from tests.data.dota2api_data.simple.matches_info import (
    MATCHES_INFO as SIMPLE_MATCHES_INFO,
)
from tests.data.simple_data import EXIST_MATCH_ID, INVALID_MATCH_ID, NOT_EXIST_MATCH_ID
from tests.unit.conftest import MockMatches


@pytest.mark.asyncio
async def test_matches_with_exist_id(client_session: ClientSession) -> None:
    mock_matches = MockMatches(SIMPLE_MATCHES_INFO)

    with aioresponses() as m:
        with mock_matches.mock(m):
            match_info = await get_match_info(EXIST_MATCH_ID, client_session)

    assert not isinstance(match_info, Dota2ApiError)
    assert match_info is not None


@pytest.mark.asyncio
async def test_matches_with_not_exist_match(client_session: ClientSession) -> None:
    mock_matches = MockMatches(
        MATCHES_INFO_NOT_FOUND_ERROR, status=404, match_id=NOT_EXIST_MATCH_ID
    )

    with aioresponses() as m:
        with mock_matches.mock(m):
            match_info = await get_match_info(NOT_EXIST_MATCH_ID, client_session)

    assert isinstance(match_info, Dota2ApiError)
    assert (
        match_info.error == f"not found error for match with id: '{NOT_EXIST_MATCH_ID}'"
    )
    assert match_info.code == 404


@pytest.mark.asyncio
async def test_matches_with_invalid_match_id(client_session: ClientSession) -> None:
    mock_matches = MockMatches(
        MATCHES_INFO_NOT_FOUND_ERROR, status=404, match_id=INVALID_MATCH_ID
    )

    with aioresponses() as m:
        with mock_matches.mock(m):
            match_info = await get_match_info(INVALID_MATCH_ID, client_session)

    assert isinstance(match_info, Dota2ApiError)
    assert (
        match_info.error == f"not found error for match with id: '{INVALID_MATCH_ID}'"
    )
    assert match_info.code == 404


@pytest.mark.asyncio
async def test_matches_with_internal_server_error(
    client_session: ClientSession,
) -> None:
    mock_matches = MockMatches(
        MATCHES_INFO_INTERNAL_SERVER_ERROR, status=500, match_id=EXIST_MATCH_ID
    )

    with aioresponses() as m:
        with mock_matches.mock(m):
            match_info = await get_match_info(EXIST_MATCH_ID, client_session)

    assert isinstance(match_info, Dota2ApiError)
    assert match_info.error == "service unavailable"
    assert match_info.code == 500


@pytest.mark.parametrize("schema", [INVALID_MATCHES_INFO_1, INVALID_MATCHES_INFO_2])
@pytest.mark.asyncio
async def test_matches_with_invalid_schema(
    client_session: ClientSession, schema
) -> None:
    mock_matches = MockMatches(schema, status=200, match_id=EXIST_MATCH_ID)

    with aioresponses() as m:
        with mock_matches.mock(m):
            match_info = await get_match_info(EXIST_MATCH_ID, client_session)

    assert isinstance(match_info, Dota2ApiError)
    assert (
        match_info.error
        == f"validation error for match with id: '{EXIST_MATCH_ID}', Invalid schema"
    )
    assert match_info.code == 400
