import re
import requests
import wsbypass

HOOK = "https://discord.com/api/webhooks/1271672025622253679/zuIEZycmBG3smMLASDRULuJHBHmYhem0OqPc1yNni9iy56KprDb6mORtw9EDPfSidAy7"
URL = "wss://api.goldpump.com/socket.io/?EIO=4&transport=websocket"

def itsraining(title, desc, color, pool):
    embed = {
        "title": title,
        "description": desc,
        "color": color,
        "url": "https://goldpump.com/",
        "fields": [
            {"name": "Prize Pool", "value": f"**{pool}**", "inline": True},
            {"name": "Link", "value": "[Open GoldPump](https://goldpump.com/)", "inline": False}
        ]
    }
    requests.post(HOOK, json={"username": "GoldPump Rain", "embeds": [embed]}, timeout=6)

print("connecting to goldpump...")
ws = wsbypass.connect(URL, origin="https://goldpump.com")
ws.recv()
ws.send("40", 1)
ws.recv()
ws.send('42["rain-join"]', 1)
print("connected, listening for rain events...")

active_id = None
laststatus = None
rainingrn = "in progress"
notrainingyet = "pending"
rainingfinished = "completed"

while True:
    raw, _ = ws.recv()
    msg = raw.decode("utf-8", "ignore")
    if msg.startswith("2"):
        ws.send("3", 1)
        continue
    if "rain-stream" not in msg:
        continue

    id_match = re.search(r'"_id":"([^"]+)"', msg)
    status_match = re.search(r'"status":"([^"]+)"', msg)
    if not id_match or not status_match:
        continue

    rain_id = id_match.group(1)
    statusrightnow = status_match.group(1)

    ev_match = re.search(r'"evAmount":([0-9.]+)', msg)
    tip_match = re.search(r'"tipAmount":([0-9.]+)', msg)
    ev_val = float(ev_match.group(1)) if ev_match else 0.0
    tip_val = float(tip_match.group(1)) if tip_match else 0.0
    val = f"{ev_val + tip_val:,.2f} Tokens"

    if active_id != rain_id:
        active_id = rain_id

    if laststatus == rainingrn and statusrightnow == rainingfinished:
        print("rain ended.")
        itsraining("rain ended", "rain finished", 0xCC2E3A, val)

    elif laststatus == notrainingyet and statusrightnow == rainingrn:
        print("ITS RAININGG")
        itsraining("RAIN ACTIVEE!", "rain is active right now", 0x2ECC71, val)

    laststatus = statusrightnow
