from telethon import TelegramClient
from collections import defaultdict
import json
import os

# Read secrets from environment (GitHub Secrets)
api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
group = os.environ["GROUP"]

# Initialize Telethon client
client = TelegramClient("session", api_id, api_hash)

# Load last processed message ID
try:
    with open("last_id.txt") as f:
        last_id = int(f.read().strip())
except:
    last_id = 0

# Load existing cumulative stats
try:
    with open("stats.json") as f:
        stats = json.load(f)
except:
    stats = {}

new_last_id = last_id

async def main():
    global new_last_id
    # Iterate over new messages only
    async for msg in client.iter_messages(group, min_id=last_id):
        if not msg.sender:
            continue
        user = msg.sender.username or f"id_{msg.sender_id}"
        stats[user] = stats.get(user, 0) + 1
        new_last_id = max(new_last_id, msg.id)

    # Save updated stats
    with open("stats.json", "w") as f:
        json.dump(stats, f, indent=2)

    # Save last processed message ID
    with open("last_id.txt", "w") as f:
        f.write(str(new_last_id))

with client:
    client.loop.run_until_complete(main())
