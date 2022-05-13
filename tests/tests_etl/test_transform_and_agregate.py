from src.etl.pipeline import agregate_all_transformed_data, transform
from tests.dummy_data.pipeline_data_1 import KDA_AND_KP_LIST_1, MATCHES_1


def test_transform_and_agregate_simple() -> None:
    measure_kda_and_kp_list = []

    for match, real_kda_and_kp in zip(MATCHES_1, KDA_AND_KP_LIST_1):
        measure_kda_and_kp = transform("1", match)

        assert measure_kda_and_kp == real_kda_and_kp

        measure_kda_and_kp_list.append(measure_kda_and_kp)

    data_to_locate = agregate_all_transformed_data(
        "dummy_game", "dummy_player_name", 2, measure_kda_and_kp_list
    )

    assert data_to_locate["game"] == "dummy_game"
    assert data_to_locate["player"] == "dummy_player_name"
    assert data_to_locate["total_games"] == 2

    assert data_to_locate["max_kda"] == 3.0
    assert data_to_locate["min_kda"] == 1.5
    assert data_to_locate["avg_kda"] == 2.25

    assert data_to_locate["max_kp"] == "180.0%"
    assert data_to_locate["min_kp"] == "150.0%"
    assert data_to_locate["avg_kp"] == "165.0%"
