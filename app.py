import json
import os
import socket
import struct
import subprocess
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "computers.json")


def load_computers():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_computers(computers):
    with open(DATA_FILE, "w") as f:
        json.dump(computers, f, indent=2)


def is_online(ip):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", ip],
            capture_output=True,
            timeout=5,
        )
        return result.returncode == 0
    except Exception:
        return False


def send_wol(mac, broadcast="255.255.255.255", port=9):
    mac_bytes = bytes(int(b, 16) for b in mac.replace(":", "-").split("-"))
    packet = b"\xff" * 6 + mac_bytes * 16
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(packet, (broadcast, port))
    sock.close()
    return True


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/computers", methods=["GET"])
def get_computers():
    computers = load_computers()
    for c in computers:
        c["online"] = is_online(c["ip"])
    return jsonify(computers)


@app.route("/api/computers", methods=["POST"])
def add_computer():
    data = request.json
    computers = load_computers()
    computers.append({
        "id": len(computers) + 1,
        "name": data["name"],
        "ip": data["ip"],
        "mac": data["mac"],
    })
    save_computers(computers)
    return jsonify({"id": computers[-1]["id"]}), 201


@app.route("/api/computers/<int:cid>", methods=["DELETE"])
def delete_computer(cid):
    computers = load_computers()
    computers = [c for c in computers if c["id"] != cid]
    save_computers(computers)
    return jsonify({"ok": True})


@app.route("/api/wake/<int:cid>", methods=["POST"])
def wake_computer(cid):
    computers = load_computers()
    computer = next((c for c in computers if c["id"] == cid), None)
    if not computer:
        return jsonify({"error": "Not found"}), 404
    send_wol(computer["mac"])
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
