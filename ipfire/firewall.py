import datetime

logfile = "./firewall.log"
today = datetime.datetime.now().strftime("%b %d")

unique_ips = set()
total_drop_hostile = 0

with open(logfile, "r") as f:
    for line in f:
        if today in line and "DROP_HOSTILE" in line:
            total_drop_hostile += 1
            # Extract SRC IP
            parts = line.split()
            for part in parts:
                if part.startswith("SRC="):
                    ip = part.split("=")[1]
                    unique_ips.add(ip)
                    break

print(f"Total DROP_HOSTILE entries today: {total_drop_hostile}")
print(f"Unique SRC IPs today: {len(unique_ips)}")
print("Unique IPs:")
for ip in unique_ips:
    print(ip)