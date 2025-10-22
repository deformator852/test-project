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

### 1. Create virtual environments

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
