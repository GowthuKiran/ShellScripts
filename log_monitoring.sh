# This script to monitor log in real-time and notify the users
# Author: KiranKumar Chintha

#!/bin/bash
LOG_FILE="/home/ubuntu/cnapp.log"
Error_pattern=("ERROR", "WARN", "INFO")

# function to send alert or notify user incase error matches

send_alert()
{

    local message=$1
    echo "[$(date)]:ALERT: $messgae"
}

# real-time monitoring of the error log

tail -F "$LOG_FILE" | while read -r line; 
do
    for pattern in "${Error_pattern[@]}"; do
        if echo "$line" | grep -q "$pattern"; then
            send_alert "Pattern $pattern found in log: $line"
        fi
    done
done


