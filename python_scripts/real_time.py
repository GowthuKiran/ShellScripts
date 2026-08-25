#!/usr/bin/env python3
from __future__ import annotations
import glob
import pwd
import subprocess


print("🔹 1. Loop through servers and run uptime")
servers = ["server1", "server2", "server3"]
for server in servers:
    print(f"Would run uptime on {server} (mock)")
print("---------------------------------------------")

print("🔹 2. Loop through log files and search for errors")
for logfile in glob.glob("/var/log/*.log"):
    print(f"Scanning {logfile}")
    try:
        with open(logfile, "r", encoding="utf-8", errors="replace") as f:
            content = f.read().lower()
        if "error" in content:
            print(f"  ❌ Error found in {logfile}")
        else:
            print(f"  ✅ No errors in {logfile}")
    except OSError:
        print(f"  ⚠️ Could not read {logfile}")
print("---------------------------------------------")

print("🔹 3. Loop through users and check existence")
users = ["alice", "bob", "charlie"]
for user in users:
    try:
        pwd.getpwnam(user)
        print(f"✅ User {user} exists")
    except KeyError:
        print(f"❌ User {user} does not exist — would create here")
print("---------------------------------------------")

print("🔹 4. Loop through services and check if running")
services = ["sshd", "nginx", "docker"]
for service in services:
    status = subprocess.run(["systemctl", "is-active", "--quiet", service]).returncode
    if status == 0:
        print(f"✅ {service} is running")
    else:
        print(f"❌ {service} is not running, would start here")
print("---------------------------------------------")
