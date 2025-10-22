import argparse
import asyncio
import random
from datetime import datetime

import aiohttp


def parse_args():
    parser = argparse.ArgumentParser(description="Sensor Node")
    parser.add_argument("--sensor-name", required=True, help="Sensor name")
    parser.add_argument(
        "--rate", type=float, default=1.0, help="Frequency of sending messages"
    )
    parser.add_argument(
        "--sink-url", required=True, help="URL of the telemetry receiver"
    )
    return parser.parse_args()


async def send_telemetry(session, sink_url, payload):
    try:
        async with session.post(sink_url, json=payload, timeout=3) as response:
            if response.status != 200:
                print(f"[WARN] Sink responded with {response.status}")
    except Exception as e:
        print(f"[ERROR] Failed to send telemetry: {e}")


async def sensor_loop(sensor_name: str, rate: float, sink_url: str):
    interval = 1.0 / rate
    async with aiohttp.ClientSession() as session:
        while True:
            payload = {
                "sensor_name": sensor_name,
                "value": random.randint(0, 100),
                "timestamp": datetime.now().isoformat() + "z",
            }
            print(f"[{datetime.now().isoformat()}] Sending: {payload}")
            await send_telemetry(session, sink_url, payload)
            await asyncio.sleep(interval)


async def main():
    args = parse_args()
    print(
        f"Starting sensor '{args.sensor_name}' → {args.sink_url} (rate={args.rate}/s)"
    )
    try:
        await sensor_loop(args.sensor_name, args.rate, args.sink_url)
    except asyncio.CancelledError:
        print("Sensor stopped.")


if __name__ == "__main__":
    asyncio.run(main())
