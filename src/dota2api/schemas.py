MATHES_SCHEMA = {
    "type": "object",
    "properties": {
        "match_id": {"type": "number"},
        "players": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "account_id": {"type": ["number", "null"]},
                    "kills": {"type": "number"},
                    "assists": {"type": "number"},
                    "deaths": {"type": "number"},
                    "isRadiant": {"type": "boolean"},
                },
                "required": ["account_id", "kills", "assists", "deaths", "isRadiant"],
            },
        },
    },
    "required": ["match_id", "players"],
}

PLAYERS_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "match_id": {"type": "number"},
        },
        "required": ["match_id"],
    },
}
