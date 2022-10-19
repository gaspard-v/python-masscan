from typing import List, Callable, Awaitable

GENERAL_CALLBACK = Callable[[str, str], List[Awaitable[None]]]
SPECIAL_CALLBACK = Callable[[dict, str], List[Awaitable[None]]]


class data_saver:
    def __init__(self, general_callbacks: List[GENERAL_CALLBACK] = [], special_callbacks: List[SPECIAL_CALLBACK] = []):
        self.general_callbacks = general_callbacks
        self.special_callbacks = special_callbacks

    async def add_general_callbacks(self, general_callbacks: List[GENERAL_CALLBACK]):
        self.general_callbacks += general_callbacks

    async def add_special_callbacks(self, special_callbacks: List[SPECIAL_CALLBACK]):
        self.special_callbacks += special_callbacks

    async def general_save(self, data: str, filename: str) -> List[Awaitable[None]]:
        return [callback(data, filename) for callback in self.general_callbacks]

    async def special_save(self, data: dict, filename: str) -> List[Awaitable[None]]:
        return [callback(data, filename) for callback in self.special_callbacks]
