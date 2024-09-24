import asyncio

from bot import *

loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())
