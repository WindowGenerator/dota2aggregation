from typing import Dict, List, Tuple

from aiohttp import ClientSession
from src.dota2api.matches import get_match_info
from src.dota2api.recent_matches import get_recent_mathes_by_account
from src.dota2api.types import AccountId, Dota2ApiError


INT_MAX = 2**32 - 1

KDA_AndAllKills = Tuple[int, int, int, int]
KDA = float
KP = float


class TransformError(Exception):
    pass


class PipelineError(Exception):
    pass


async def pipeline(
    client_session: ClientSession,
    account_id: AccountId,
    player_name: str,
    limit: int = 10,
) -> Dict:
    kda_and_kp_list = []
    total_games = 0

    try:
        async for match_info in extract(client_session, account_id, limit):
            kda_and_kp_list.append(transform(account_id, match_info))
            total_games += 1

        data_to_locate = agregate_all_transformed_data(
            "Dota", player_name, total_games, kda_and_kp_list
        )

        await locate(account_id, data_to_locate)

    except TransformError as exc:
        raise PipelineError(exc)

    except Dota2ApiError as exc:
        raise PipelineError(exc.error)

    return data_to_locate


async def locate(account_id: AccountId, data_to_locate: Dict) -> None:
    print(data_to_locate)


def transform(account_id: AccountId, match_info: Dict) -> Tuple[KDA, KP]:
    # Here I decided to use a tuple,
    # because I thought in advance about the performance when allocating memory for other data structures,
    # and python allocates much less memory for a tuple than for the same NamedTuple

    kills, deaths, assists = None, None, None
    is_radiant = None

    kills_dire = 0
    kills_radiant = 0

    for player in match_info["players"]:
        if player["isRadiant"]:
            kills_radiant += player["kills"]
        else:
            kills_dire += player["kills"]

        if str(player["account_id"]) == str(account_id):
            kills, deaths, assists = (
                player["kills"],
                player["deaths"],
                player["assists"],
            )
            is_radiant = player["isRadiant"]

    if is_radiant is None:
        raise TransformError(
            f"Unable to find account id: {account_id} belonging to the owner"
        )

    kda = (kills + assists) / max(deaths, 1)
    kp = ((kills + assists) / max(kills_radiant if is_radiant else kills_dire, 1)) * 100

    return kda, kp


def agregate_all_transformed_data(
    game: str, player_name: str, total_games: int, kda_and_kp_list: List[Tuple[KDA, KP]]
) -> Dict:

    max_kda, min_kda, avg_kda = 0, INT_MAX, 0
    max_kp, min_kp, avg_kp = 0, INT_MAX, 0

    for kda_and_kp in kda_and_kp_list:
        kda, kp = kda_and_kp

        if kda > max_kda:
            max_kda = kda
        if kda < min_kda:
            min_kda = kda

        if kp > max_kp:
            max_kp = kp
        if kp < min_kp:
            min_kp = kp

        avg_kda += kda
        avg_kp += kp

    return {
        "game": game,
        "player": player_name,
        "total_games": total_games,
        "max_kda": round(max_kda, 2),
        "min_kda": round(min_kda, 2),
        "avg_kda": round(avg_kda / total_games, 2),
        "max_kp": f"{round(max_kp, 2)}%",
        "min_kp": f"{round(min_kp, 2)}%",
        "avg_kp": f"{round(avg_kp / total_games, 2)}%",
    }


async def extract(
    client_session: ClientSession, account_id: AccountId, limit: int
) -> Dict:
    matches = await get_recent_mathes_by_account(
        account_id, client_session, limit=limit
    )

    if isinstance(matches, Dota2ApiError):
        raise matches

    for match in matches:
        match_id = match["match_id"]

        match_info = await get_match_info(match_id, client_session)

        if isinstance(match_info, Dota2ApiError):
            raise matches

        yield match_info
