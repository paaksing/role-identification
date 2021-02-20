import asyncio
from functools import partial
from typing import List, Dict
from datetime import datetime, timedelta


async def thread_run(func, *args, **kwargs):
    '''Run a blocking function in a thread.'''
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, partial(func, *args, **kwargs))


def get_most_played(champion_roles: Dict, role: str, champs: List[int]) -> int:
    highest = 0.3
    identified = None
    for champ in champs:
        playrate = champion_roles[champ][role]
        if playrate > highest:
            highest = playrate
            identified = champ
    return identified


class AutoData:

    def __init__(self, func, interval=60*60*3):
        self.interval = interval
        self.func = func
        self.data = None
        self.next_update = datetime.now()
        self.updating = False

    def get(self):
        if self.next_update < datetime.now() and not self.updating:
            self.updating = True
            self.data = self.func()
            self.updating = False
            self.next_update = datetime.now() + timedelta(seconds=self.interval)
        return self.data

    async def aget(self):
        if self.next_update < datetime.now() and not self.updating:
            self.updating = True
            self.data = await thread_run(self.func)
            self.updating = False
            self.next_update = datetime.now() + timedelta(seconds=self.interval)
        return self.data
