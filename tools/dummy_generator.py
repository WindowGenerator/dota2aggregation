import asyncio
import os

from typing import List

from aiohttp import ClientSession
from src.dota2api.matches import get_match_info
from src.dota2api.recent_matches import get_recent_mathes_by_account


def convert_and_write_matches(
    matches_info: List, dir_to_write: str = "./tools"
) -> None:
    converted_mathes_info = []

    for match_info in matches_info:
        players = []
        for player in match_info["players"]:
            players.append(
                {
                    "account_id": player["account_id"],
                    "kills": player["kills"],
                    "assists": player["assists"],
                    "deaths": player["deaths"],
                    "isRadiant": player["isRadiant"],
                }
            )

        converted_mathes_info.append(
            {
                "players": players,
            }
        )

    with open(os.path.join(dir_to_write, "matches_info.py"), "wt") as file_fd:
        file_fd.write(f"MATCHES_INFO={str(converted_mathes_info)}")


def convert_and_write_account_matches(
    account_matches: List, dir_to_write: str = "./tools"
) -> None:
    converted_account_matches = []

    for match in account_matches:
        converted_account_matches.append({"match_id": match["match_id"]})

    with open(os.path.join(dir_to_write, "recent_matches.py"), "wt") as file_fd:
        file_fd.write(f"RECENT_MATCHES={str(converted_account_matches)}")


async def main() -> None:
    dir_to_write = "./tests_data/dota2api_data/simple"
    account_id = "70388657"
    limit = 10

    async with ClientSession() as client:
        os.makedirs(dir_to_write, exist_ok=True)
        open(os.path.join(dir_to_write, "__init__.py"), "a").close()

        account_matches = await get_recent_mathes_by_account(
            account_id=account_id, client_session=client, limit=limit
        )

        convert_and_write_account_matches(account_matches, dir_to_write=dir_to_write)

        mathes_info = []

        for match in account_matches:
            match_id = match["match_id"]

            mathes_info.append(await get_match_info(match_id, client))

        convert_and_write_matches(mathes_info, dir_to_write=dir_to_write)


if __name__ == "__main__":
    asyncio.run(main())
