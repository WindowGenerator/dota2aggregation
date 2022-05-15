MATHES_SCHEMA = {
    "type": "object",
    "properties": {
        "players": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "account_id": {"type": ["number", "null"]},
                    "name": {"type": ["string", "null"]},
                    "kills": {"type": "number"},
                    "assists": {"type": "number"},
                    "deaths": {"type": "number"},
                    "isRadiant": {"type": "boolean"},
                },
            },
        }
    },
}

PLAYERS_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "match_id": {"type": "number"},
        },
    },
}
