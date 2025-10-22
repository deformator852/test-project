# Telemetry Project

This project implements a simple telemetry system consisting of a **Sensor Node** and a **Telemetry Sink**.  

- **Sensor Node**: simulates a sensor generating telemetry data at a configurable rate.  
- **Telemetry Sink**: receives, encrypts, buffers, and stores telemetry data.  

---

## Prerequisites

- Python 3.11+ (tested in venv)
- `pip` package manager

---

## Setup

```bash
# Telemetry Sink
cd telemetry_sink
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Sensor Node
cd ../sensor_node
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

### Sensor Node
```bash
cd sensor_node
source venv/bin/activate
python main.py \
  --sensor-name sensor1 \
  --rate 1 \
  --sink-url http://localhost:8080/telemetry
```

### Telemetry sink
```bash
cd telemetry_sink
source venv/bin/activate
python main.py \
  --bind 0.0.0.0:8080 \
  --log-path telemetry.log \
  --buffer-size 4096 \
  --flush-interval 0.5 \
  --rate-limit 10240 \
```
