# Wake on LAN

A web-based Wake-on-LAN controller. Add computers by name, IP, and MAC address, check their online status, and send magic packets to wake them up.

## Features

- Add / remove computers (name, IP, MAC address)
- Live online/offline status (ping check, refreshes every 15 seconds)
- One-click Wake-on-LAN magic packet
- Persistent storage (JSON file)
- Dark-themed, responsive UI

## Quick Start — Docker

### 1. Build the image

```bash
docker build -t wakeonlan .
```

### 2. Run the container

```bash
docker run -d \
  --name wakeonlan \
  --network host \
  -v $(pwd)/data:/app/data \
  -e DATA_FILE=/app/data/computers.json \
  --restart unless-stopped \
  wakeonlan
```

> **`--network host`** is required so the container can send UDP broadcast packets to wake machines on your local network.

### 3. Open in browser

Navigate to `http://<your-server-ip>:5000`.

### 4. Stop / remove

```bash
docker stop wakeonlan
docker rm wakeonlan
```

## Quick Start — Bare Metal (no Docker)

### 1. Install dependencies

```bash
pip install flask
```

### 2. Run

```bash
python3 app.py
```

### 3. Open in browser

Navigate to `http://localhost:5000`.

## Docker Compose

Save this as `docker-compose.yml`:

```yaml
services:
  wakeonlan:
    build: .
    container_name: wakeonlan
    network_mode: host
    restart: unless-stopped
    volumes:
      - ./data:/app/data
    environment:
      - DATA_FILE=/app/data/computers.json
```

Then:

```bash
docker compose up -d --build
```

## Configuration

### Data file location

Computers are stored in `computers.json` (or the path set via `DATA_FILE`).

| Method       | Default Path            |
|--------------|-------------------------|
| Bare metal   | `./computers.json`      |
| Docker       | `/app/computers.json`   |

To persist data in Docker, mount a volume to the directory containing the file.

### Broadcast address

The magic packet is sent to `255.255.255.255:9` by default. If your network requires a specific broadcast address, modify the `broadcast` argument in `send_wol()` inside `app.py`.

### Port

The app listens on port `5000`. Change it in the `app.run()` call:

```python
app.run(host="0.0.0.0", port=5000, debug=True)
```

## Requirements

- Python 3.12+ (bare metal)
- Docker 24+ (containerized)
- `ping` utility available in the container/image (included in the `python:3.12-slim` base image)

## Wake-on-LAN prerequisites

For WoL to work on the target machine:

1. **Enable WoL in BIOS/UEFI** — look for "Wake on LAN", "PME Event Wakeup", or similar.
2. **Enable WoL in the OS** — on Linux: `ethtool eth0 | grep Wake-on` (set with `sudo ethtool -s eth0 wol g`). On Windows: Device Manager → Network Adapter → Power Management → "Allow this device to wake the computer".
3. **Connect via Ethernet** — WoL over Wi-Fi is not supported by most hardware.
4. **Same network** — the WoL packet must reach the target machine's network segment.
# wakeonlan
# wakeonlan
# wakeonlan
