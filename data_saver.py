from typing import List, Callable, Awaitable

GENERAL_CALLBACK = Callable[[str, str], Awaitable[int]]
SPECIAL_CALLBACK = Callable[[dict], Awaitable[int]]


class data_saver:
    def __init__(self, general_callbacks: List[GENERAL_CALLBACK] = [], special_callbacks: List[SPECIAL_CALLBACK] = []):
        self.general_callbacks = general_callbacks
        self.special_callbacks = special_callbacks

    def add_general_callbacks(self, general_callbacks: List[GENERAL_CALLBACK]):
        self.general_callbacks += general_callbacks

    def add_special_callbacks(self, special_callbacks: List[SPECIAL_CALLBACK]):
        self.special_callbacks += special_callbacks

    def general_save(self, data: str, filename: str):
        for callback in self.general_callbacks:
            callback(data, filename)

    def special_save(self, data: dict, filename: str):
        for callback in self.special_callbacks:
            callback(data, filename)
