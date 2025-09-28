import os
import asyncio
from typing import Awaitable, Callable, Optional

try:
    import nats
except ImportError:
    nats = None

NATS_URL = os.environ.get("NATS_URL", "nats://localhost:4222")

class NATSClient:
    def __init__(self):
        self.nc: Optional["nats.NATS"] = None  # type: ignore

    async def connect(self):
        if nats is None:
            raise RuntimeError("Le paquet 'nats-py' n'est pas installé.")
        if not self.nc or not self.nc.is_connected:
            self.nc = await nats.connect(NATS_URL)

    async def publish(self, subject: str, message: bytes):
        await self.connect()
        assert self.nc is not None
        await self.nc.publish(subject, message)

    async def subscribe(self, subject: str, callback: Callable[["nats.aio.msg.Msg"], Awaitable[None]]):  # type: ignore
        await self.connect()
        assert self.nc is not None
        await self.nc.subscribe(subject, cb=callback)

    async def close(self):
        if self.nc:
            await self.nc.close()
