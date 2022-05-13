from typing import Union


MatchId = Union[str, int]
AccountId = Union[str, int]


class Dota2ApiError(Exception):
    def __init__(self, error: str, code: int, *args, **kwargs) -> None:
        super().__init__(self, *args, **kwargs)
        self.error = error
        self.code = code
