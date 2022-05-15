from src.etl.pipeline import agregate_all_transformed_data, transform
from tests.data.dota2api_data.simple.matches_info import (
    MATCHES_INFO as MATCHES_INFO_SIMPLE,
)
from tests.data.simple_data import EXIST_ACCOUNT_ID


SIMPLE_KDA_AND_KP_LIST = [
    (0.6363636363636364, 58.333333333333336),
    (20.0, 74.07407407407408),
    (21.0, 63.63636363636363),
    (2.6666666666666665, 57.14285714285714),
    (15.0, 65.21739130434783),
    (3.5, 56.75675675675676),
    (17.0, 77.27272727272727),
    (3.6666666666666665, 55.00000000000001),
    (19.0, 67.85714285714286),
    (4.0, 52.17391304347826),
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

    assert data_to_locate["max_kda"] == 21.0
    assert data_to_locate["min_kda"] == 0.64
    assert data_to_locate["avg_kda"] == 10.65

    assert data_to_locate["max_kp"] == "77.27%"
    assert data_to_locate["min_kp"] == "52.17%"
    assert data_to_locate["avg_kp"] == "62.75%"


# @pytest.skip
# @pytest.mark.asyncio
# async def test_extract_simple(client_session: ClientSession) -> None:
#     await extract(EXIST_ACCOUNT_ID, client_session)
