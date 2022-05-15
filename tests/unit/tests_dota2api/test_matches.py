import pytest

from aiohttp import ClientSession
from src.dota2api.matches import get_match_info
from src.dota2api.types import Dota2ApiError
from tests.data.dota2api_data.not_found_error import MATCHES_INFO_NOT_FOUND_ERROR
from tests.data.dota2api_data.simple.matches_info import (
    MATCHES_INFO as SIMPLE_MATCHES_INFO,
)
from tests.data.simple_data import EXIST_MATCH_ID, INVALID_MATCH_ID, NOT_EXIST_MATCH_ID
from tests.unit.conftest import MockMatches


@pytest.mark.asyncio
async def test_matches_with_exist_id(client_session: ClientSession) -> None:
    open_dota_2_mock = MockMatches(SIMPLE_MATCHES_INFO)
    client_session.get = open_dota_2_mock.mock_matches

    match_info = await get_match_info(EXIST_MATCH_ID, client_session)

    assert not isinstance(match_info, Dota2ApiError)
    assert match_info is not None


@pytest.mark.asyncio
async def test_matches_with_not_exist_match(client_session: ClientSession) -> None:
    open_dota_2_mock = MockMatches(MATCHES_INFO_NOT_FOUND_ERROR, status=404)
    client_session.get = open_dota_2_mock.mock_matches

    match_info = await get_match_info(NOT_EXIST_MATCH_ID, client_session)

    assert isinstance(match_info, Dota2ApiError)
    assert (
        match_info.error == f"not found error for match with id: '{NOT_EXIST_MATCH_ID}'"
    )
    assert match_info.code == 404


@pytest.mark.asyncio
async def test_matches_with_invalid_match_id(client_session: ClientSession) -> None:
    open_dota_2_mock = MockMatches(MATCHES_INFO_NOT_FOUND_ERROR, status=404)
    client_session.get = open_dota_2_mock.mock_matches

    match_info = await get_match_info(INVALID_MATCH_ID, client_session)

    assert isinstance(match_info, Dota2ApiError)
    assert (
        match_info.error == f"not found error for match with id: '{INVALID_MATCH_ID}'"
    )
    assert match_info.code == 404
