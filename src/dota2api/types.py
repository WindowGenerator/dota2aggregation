from typing import Union


MatchId = Union[str, int]
AccountId = Union[str, int]


class Dota2ApiError(Exception):
    def __init__(self, error: str, code: int, *args, **kwargs) -> None:
        super().__init__(self, *args, **kwargs)
        self.error = error
        self.code = code

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>, error: {self.error}, code: {self.code}"
