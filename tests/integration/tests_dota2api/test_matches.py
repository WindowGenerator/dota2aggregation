import pytest

from aiohttp import ClientSession
from src.dota2api.matches import get_match_info
from src.dota2api.types import Dota2ApiError
from tests.data.simple_data import EXIST_MATCH_ID, INVALID_MATCH_ID, NOT_EXIST_MATCH_ID


@pytest.mark.asyncio
async def test_matches_with_exist_id(client_session: ClientSession) -> None:
    match_info = await get_match_info(EXIST_MATCH_ID, client_session)

    assert not isinstance(match_info, Dota2ApiError)
    assert match_info is not None


@pytest.mark.asyncio
async def test_matches_with_not_exist_match_id(client_session: ClientSession) -> None:
    match_info = await get_match_info(NOT_EXIST_MATCH_ID, client_session)

    assert isinstance(match_info, Dota2ApiError)
    assert (
        match_info.error == f"not found error for match with id: '{NOT_EXIST_MATCH_ID}'"
    )
    assert match_info.code == 404


@pytest.mark.asyncio
async def test_matches_with_invalid_match_id(client_session: ClientSession) -> None:
    match_info = await get_match_info(INVALID_MATCH_ID, client_session)

    assert isinstance(match_info, Dota2ApiError)
    assert (
        match_info.error == f"not found error for match with id: '{INVALID_MATCH_ID}'"
    )
    assert match_info.code == 404
