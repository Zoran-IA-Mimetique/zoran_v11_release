import os
import asyncio
from typing import Callable, Awaitable, Optional
import nats

NATS_URL = os.environ.get("NATS_URL", "nats://localhost:4222")

class NATSClient:
    def __init__(self) -> None:
        self.nc: Optional[nats.NATS] = None

    async def connect(self) -> None:
        if not self.nc or not self.nc.is_connected:
            self.nc = await nats.connect(NATS_URL)

    async def publish(self, subject: str, message: bytes) -> None:
        await self.connect()
        assert self.nc is not None
        await self.nc.publish(subject, message)

    async def subscribe(self, subject: str, callback: Callable[[nats.aio.msg.Msg], Awaitable[None]]) -> None:
        await self.connect()
        assert self.nc is not None
        await self.nc.subscribe(subject, cb=callback)

    async def close(self) -> None:
        if self.nc:
            await self.nc.close()
