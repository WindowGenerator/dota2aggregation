import pytest

from aiohttp import ClientSession
from aioresponses import aioresponses
from src.etl.pipeline import agregate_all_transformed_data, pipeline, transform
from tests.data.dota2api_data.simple.matches_info import (
    MATCHES_INFO as MATCHES_INFO_SIMPLE,
)
from tests.data.dota2api_data.simple.recent_matches import (
    RECENT_MATCHES as RECENT_MATCHES_SIMPLE,
)
from tests.data.simple_data import EXIST_ACCOUNT_ID
from tests.unit.conftest import MockMatches, MockRecentMatches


SIMPLE_KDA_AND_KP_LIST = [
    (2.2857142857142856, 72.72727272727273),
    (8.5, 62.96296296296296),
    (2.6, 59.09090909090909),
    (0.7777777777777778, 63.63636363636363),
    (1.0, 50.0),
    (0.7142857142857143, 41.66666666666667),
    (4.333333333333333, 52.0),
    (22.0, 68.75),
    (3.5, 58.333333333333336),
    (1.0, 55.55555555555556),
]


def test_transform_and_agregate_simple() -> None:
    measure_kda_and_kp_list = []

    for match, real_kda_and_kp in zip(MATCHES_INFO_SIMPLE, SIMPLE_KDA_AND_KP_LIST):
        measure_kda_and_kp = transform(EXIST_ACCOUNT_ID, match)

        assert measure_kda_and_kp == real_kda_and_kp

        measure_kda_and_kp_list.append(measure_kda_and_kp)

    data_to_locate = agregate_all_transformed_data(
        "dummy_game", "dummy_player_name", 10, measure_kda_and_kp_list
    )

    assert data_to_locate["game"] == "dummy_game"
    assert data_to_locate["player"] == "dummy_player_name"
    assert data_to_locate["total_games"] == 10

    assert data_to_locate["max_kda"] == 22.0
    assert data_to_locate["min_kda"] == 0.71
    assert data_to_locate["avg_kda"] == 4.67

    assert data_to_locate["max_kp"] == "72.73%"
    assert data_to_locate["min_kp"] == "41.67%"
    assert data_to_locate["avg_kp"] == "58.47%"


@pytest.mark.asyncio
async def test_pipeline_simple(client_session: ClientSession) -> None:
    mock_recent_matches = MockRecentMatches(EXIST_ACCOUNT_ID, RECENT_MATCHES_SIMPLE)
    mock_matches = MockMatches(MATCHES_INFO_SIMPLE)

    with aioresponses() as m:
        with mock_recent_matches.mock(m):
            with mock_matches.mock(m):
                await pipeline(client_session, EXIST_ACCOUNT_ID, "test")
