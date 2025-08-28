#!/bin/bash
# ====================================================
# DevOps Looping Examples in Bash
# ====================================================

echo "🔹 1. Loop through servers and run uptime"
servers=("server1" "server2" "server3")
for srv in "${servers[@]}"
do
    echo "Would run uptime on $srv (mock)"
    # ssh ubuntu@"$srv" "uptime"
done
echo "---------------------------------------------"


echo "🔹 2. Loop through log files and search for errors"
for logfile in /var/log/*.log
do
    echo "Scanning $logfile"
    if grep -qi "error" "$logfile"; then
        echo "  ❌ Error found in $logfile"
    else
        echo "  ✅ No errors in $logfile"
    fi
done
echo "---------------------------------------------"


echo "🔹 3. Loop through users and check existence"
users=("alice" "bob" "charlie")
for u in "${users[@]}"
do
    if id "$u" &>/dev/null; then
        echo "✅ User $u exists"
    else
        echo "❌ User $u does not exist — would create here"
        # sudo useradd -m "$u"
    fi
done
echo "---------------------------------------------"


echo "🔹 4. Loop through services and check if running"
services=("sshd" "nginx" "docker")
for svc in "${services[@]}"
do
    if systemctl is-active --quiet "$svc"; then
        echo "✅ $svc is running"
    else
        echo "❌ $svc is not running, would start here"
        # sudo systemctl start "$svc"
    fi
done
echo "---------------------------------------------"


echo "🔹 5. Loop through config fil
