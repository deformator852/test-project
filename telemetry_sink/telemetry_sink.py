import asyncio
import json
import time


class TelemetrySink:
    def __init__(
            self, log_path: str, buffer_size: int, flush_interval: float, rate_limit: int
    ):
        self.log_path = log_path
        self.buffer_size = buffer_size
        self.flush_interval = flush_interval
        self.rate_limit = rate_limit

        self.buffer = bytearray()
        self.lock = asyncio.Lock()
        self.last_flush = time.time()

        self.bytes_received = 0
        self.rate_window_start = time.time()

        self._shutdown_event = asyncio.Event()
        self._task = asyncio.create_task(self._periodic_flush())

    async def _periodic_flush(self):
        while not self._shutdown_event.is_set():
            await asyncio.sleep(self.flush_interval)
            await self.flush()

    async def add_message(self, data: dict) -> bool:
        msg = json.dumps(data, ensure_ascii=False) + "\n"
        msg_bytes = msg.encode("utf-8")

        now = time.time()
        if now - self.rate_window_start >= 1.0:
            self.bytes_received = 0
            self.rate_window_start = now

        if self.bytes_received + len(msg_bytes) > self.rate_limit:
            print("[WARN] Incoming rate exceeded, message dropped.")
            return False

        self.bytes_received += len(msg_bytes)

        async with self.lock:
            if len(self.buffer) + len(msg_bytes) > self.buffer_size:
                await self.flush()
            self.buffer.extend(msg_bytes)

        return True

    async def flush(self):
        async with self.lock:
            if not self.buffer:
                return
            with open(self.log_path, "ab") as f:
                f.write(self.buffer)
            print(f"[INFO] Flushed {len(self.buffer)} bytes to {self.log_path}")
            self.buffer.clear()
            self.last_flush = time.time()

    async def shutdown(self):
        print("[INFO] Shutting down TelemetrySink...")
        self._shutdown_event.set()
        await self._task
        await self.flush()
        print("[INFO] TelemetrySink shutdown complete.")
