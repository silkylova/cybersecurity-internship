import json
from collections import Counter

with open("honeypot_log.jsonl") as f:
    entries = [json.loads(line) for line in f]

print(f"Total captured clicks: {len(entries)}\n")

# Unique visitors by IP
ips = Counter(e["ip"] for e in entries)
print("Clicks by source IP:")
for ip, count in ips.most_common():
    print(f"  {ip}: {count}")

# Bait link popularity
paths = Counter(e["path"].split("?")[0] for e in entries)
print("\nMost-clicked bait links:")
for path, count in paths.most_common():
    print(f"  {path}: {count}")

# Devices / platforms
def classify_agent(agent):
    a = agent.lower()
    if "curl" in a or "wget" in a or "python" in a:
        return "Automated tool / scanner (non-human)"
    if "iphone" in a or "android" in a:
        return "Mobile device"
    if "windows" in a:
        return "Windows desktop"
    if "macintosh" in a:
        return "macOS desktop"
    if "linux" in a:
        return "Linux desktop"
    return "Unknown"

devices = Counter(classify_agent(e["agent"]) for e in entries)
print("\nDevice/platform breakdown:")
for d, count in devices.most_common():
    print(f"  {d}: {count}")

# Entry point: did they arrive via a referring page (watering hole) or direct (e.g. email)?
via_referer = sum(1 for e in entries if e["referer"] != "-")
direct = len(entries) - via_referer
print(f"\nArrived via referring page (watering-hole style): {via_referer}")
print(f"Arrived with no referer (e.g. email/IM bait link): {direct}")
