from tests.data.simple_data import EXIST_MATCH_ID


MATCHES_INFO_1 = [
    {
        "match_id": EXIST_MATCH_ID,
        "players": [
            {
                "account_id": 86745912,
                "dummmmmmy": 8,
                "assists": 8,
                "deaths": 7,
                "isRadiant": True,
            }
        ],
    }
]

MATCHES_INFO_2 = [
    {
        "match_id": EXIST_MATCH_ID,
        "players": [
            {
                "account_id": "86745912",
                "kills": 8,
                "assists": 8,
                "deaths": 7,
                "isRadiant": True,
            }
        ],
    }
]
