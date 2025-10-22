import argparse
import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request, Response

from telemetry_sink import TelemetrySink


@asynccontextmanager
async def lifespan(app: FastAPI):
    cfg = app.state.config

    sink = TelemetrySink(
        log_path=cfg["log_path"],
        buffer_size=cfg["buffer_size"],
        flush_interval=cfg["flush_interval"],
        rate_limit=cfg["rate_limit"],
    )
    app.state.sink = sink
    print(f"[INFO] TelemetrySink started (log: {cfg['log_path']})")

    try:
        yield
    finally:
        await sink.shutdown()
        print("[INFO] TelemetrySink stopped.")


app = FastAPI(title="Telemetry Sink", lifespan=lifespan)


@app.post("/telemetry")
async def receive_telemetry(request: Request):
    try:
        data = await request.json()
    except Exception:
        return Response("Invalid JSON", status_code=400)

    ok = await app.state.sink.add_message(data)
    if not ok:
        return Response("Rate limit exceeded", status_code=429)
    return Response("OK", status_code=200)


async def main():
    parser = argparse.ArgumentParser(description="Telemetry Sink Service (FastAPI)")
    parser.add_argument("--bind", default="0.0.0.0:8080", help="Address and port")
    parser.add_argument("--log-path", default="telemetry.log", help="Path to log file")
    parser.add_argument("--buffer-size", type=int, default=4096, help="Buffer size")
    parser.add_argument(
        "--flush-interval",
        type=float,
        default=0.5,
        help="Интервал сброса буфера (сек.)",
    )
    parser.add_argument(
        "--rate-limit", type=int, default=10240, help="Flow restriction (bytes/sec)"
    )
    args = parser.parse_args()

    app.state.config = {
        "log_path": args.log_path,
        "buffer_size": args.buffer_size,
        "flush_interval": args.flush_interval,
        "rate_limit": args.rate_limit,
    }

    host, port = args.bind.split(":")
    print(f"[INFO] Telemetry Sink listening on {args.bind}")

    config = uvicorn.Config(app, host=host, port=int(port), log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[INFO] Telemetry Sink stopped by user.")
