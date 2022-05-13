from typing import Dict, Union

import jsonschema

from aiohttp import ClientSession
from src.dota2api.endpoints import GET_MATCHES_URL
from src.dota2api.schemas import PLAYERS_SCHEMA
from src.dota2api.types import AccountId, Dota2ApiError


async def get_recent_mathes_by_account(
    account_id: AccountId, client_session: ClientSession, limit: int = 10
) -> Union[Dict, Dota2ApiError]:
    async with client_session.get(
        GET_MATCHES_URL.format(account_id=account_id), params={"limit": limit}
    ) as resp:
        body = await resp.json()

        if resp.status == 400:
            reason = ""

            if "error" in body:
                reason = f", reason: '{body['error']}'"

            return Dota2ApiError(
                error=f"validation error for account with id: '{account_id}'{reason}",
                code=400,
            )

        if resp.status >= 500:
            return Dota2ApiError(error="service unavailable", code=resp.status)

        if resp.status > 200:
            return Dota2ApiError(
                error=f"unexpected error for account with id: '{account_id}', status: {resp.status}",
                code=resp.status,
            )

        if not body:
            return Dota2ApiError(
                error=f"account with id: '{account_id}' not exist or account not played in dota 2",
                code=400,
            )

        try:
            jsonschema.validate(body, PLAYERS_SCHEMA)
        except jsonschema.exceptions.ValidationError as exc:
            return Dota2ApiError(
                error=f"validation error for account with id: '{account_id}'{str(exc)}",
                code=400,
            )

        return body
