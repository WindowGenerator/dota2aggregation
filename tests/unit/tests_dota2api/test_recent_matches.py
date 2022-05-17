import pytest

from aiohttp import ClientSession
from aioresponses import aioresponses
from src.dota2api.recent_matches import get_recent_mathes_by_account
from src.dota2api.types import Dota2ApiError
from tests.data.dota2api_data.internal_server_error import (
    RECENT_MATCHES_INTERNAL_SERVER_ERROR,
)
from tests.data.dota2api_data.invalid_schema.recent_matches import (
    RECENT_MATCHES_1 as INVALID_RECENT_MATCHES_1,
)
from tests.data.dota2api_data.invalid_schema.recent_matches import (
    RECENT_MATCHES_2 as INVALID_RECENT_MATCHES_2,
)
from tests.data.dota2api_data.not_exist import RECENT_MATCHES_NOT_EXIST
from tests.data.dota2api_data.simple.recent_matches import (
    RECENT_MATCHES as SIMPLE_RECENT_MATCHES,
)
from tests.data.dota2api_data.validate_error import RECENT_MATCHES_VALIDATION_ERROR
from tests.data.simple_data import (
    ACCOUNT_WITHOUT_DOTA_2_ID,
    EXIST_ACCOUNT_ID,
    INVALID_ACCOUNT_ID,
    NOT_EXIST_ACCOUNT_ID,
)
from tests.unit.conftest import MockRecentMatches


@pytest.mark.asyncio
async def test_recent_matches_with_exist_account(client_session: ClientSession) -> None:
    mock_recent_matches = MockRecentMatches(EXIST_ACCOUNT_ID, SIMPLE_RECENT_MATCHES)

    with aioresponses() as m:
        with mock_recent_matches.mock(m):
            account_info = await get_recent_mathes_by_account(
                EXIST_ACCOUNT_ID, client_session
            )

    assert not isinstance(account_info, Dota2ApiError)
    assert account_info is not None


@pytest.mark.asyncio
async def test_recent_matches_with_not_exist_acount(
    client_session: ClientSession,
) -> None:
    mock_recent_matches = MockRecentMatches(
        NOT_EXIST_ACCOUNT_ID, RECENT_MATCHES_NOT_EXIST
    )

    with aioresponses() as m:
        with mock_recent_matches.mock(m):
            account_info = await get_recent_mathes_by_account(
                NOT_EXIST_ACCOUNT_ID, client_session
            )

    assert isinstance(account_info, Dota2ApiError)
    assert (
        account_info.error
        == f"account with id: '{NOT_EXIST_ACCOUNT_ID}' not exist or account not played in dota 2"
    )
    assert account_info.code == 400


@pytest.mark.asyncio
async def test_recent_matches_with_invalid_account_id(
    client_session: ClientSession,
) -> None:
    mock_recent_matches = MockRecentMatches(
        INVALID_ACCOUNT_ID, RECENT_MATCHES_VALIDATION_ERROR, status=400
    )

    with aioresponses() as m:
        with mock_recent_matches.mock(m):
            account_info = await get_recent_mathes_by_account(
                INVALID_ACCOUNT_ID, client_session
            )

    assert isinstance(account_info, Dota2ApiError)
    assert (
        account_info.error
        == f"validation error for account with id: '{INVALID_ACCOUNT_ID}', reason: 'invalid account id'"
    )
    assert account_info.code == 400


@pytest.mark.asyncio
async def test_recent_matches_with_account_without_dota_2(
    client_session: ClientSession,
) -> None:
    mock_recent_matches = MockRecentMatches(
        ACCOUNT_WITHOUT_DOTA_2_ID, RECENT_MATCHES_NOT_EXIST
    )

    with aioresponses() as m:
        with mock_recent_matches.mock(m):
            account_info = await get_recent_mathes_by_account(
                ACCOUNT_WITHOUT_DOTA_2_ID, client_session
            )

    assert isinstance(account_info, Dota2ApiError)
    assert (
        account_info.error
        == f"account with id: '{ACCOUNT_WITHOUT_DOTA_2_ID}' not exist or account not played in dota 2"
    )
    assert account_info.code == 400


@pytest.mark.asyncio
async def test_recent_matches_with_internal_server_error(
    client_session: ClientSession,
) -> None:
    mock_recent_matches = MockRecentMatches(
        EXIST_ACCOUNT_ID, RECENT_MATCHES_INTERNAL_SERVER_ERROR, status=500
    )

    with aioresponses() as m:
        with mock_recent_matches.mock(m):
            account_info = await get_recent_mathes_by_account(
                EXIST_ACCOUNT_ID, client_session
            )

    assert isinstance(account_info, Dota2ApiError)
    assert account_info.error == "service unavailable"
    assert account_info.code == 500


@pytest.mark.parametrize("schema", [INVALID_RECENT_MATCHES_1, INVALID_RECENT_MATCHES_2])
@pytest.mark.asyncio
async def testrecent_matches_with_invalid_schema(
    client_session: ClientSession, schema
) -> None:
    mock_recent_matches = MockRecentMatches(EXIST_ACCOUNT_ID, schema, status=200)

    with aioresponses() as m:
        with mock_recent_matches.mock(m):
            account_info = await get_recent_mathes_by_account(
                EXIST_ACCOUNT_ID, client_session
            )

    assert isinstance(account_info, Dota2ApiError)
    assert (
        account_info.error
        == f"validation error for account with id: '{EXIST_ACCOUNT_ID}', Invalid schema"
    )
    assert account_info.code == 400
