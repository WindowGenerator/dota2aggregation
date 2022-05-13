from typing import Dict, Union

import jsonschema

from aiohttp import ClientSession
from src.dota2api.endpoints import GET_MATCH_URL
from src.dota2api.schemas import MATHES_SCHEMA
from src.dota2api.types import Dota2ApiError, MatchId


async def get_match_info(
    match_id: MatchId, client_session: ClientSession
) -> Union[Dict, Dota2ApiError]:
    async with client_session.get(GET_MATCH_URL.format(match_id=match_id)) as resp:
        body = await resp.json()

        if resp.status == 404:
            return Dota2ApiError(
                error=f"not found error for match with id: '{match_id}'", code=404
            )

        if resp.status >= 500:
            return Dota2ApiError(error="service unavailable", code=resp.status)

        if resp.status > 200:
            return Dota2ApiError(
                error=f"unexpected error for match with id: '{match_id}', status: {resp.status}",
                code=resp.status,
            )

        try:
            jsonschema.validate(body, MATHES_SCHEMA)
        except jsonschema.exceptions.ValidationError as exc:
            return Dota2ApiError(
                error=f"validation error for match with id: '{match_id}'{str(exc)}",
                code=400,
            )

        return body
