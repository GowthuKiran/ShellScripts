# Check if a process like nginx or sshd is running, print "Running" or "Not Running".
# Author: KiranKumar Chintha
# Date: 15-08-25
# Version: v1

#!/bin/bash

if [ -z "$1" ]; then
    echo "Uage: $0 <process name>"
    exit 1
fi

# read the process
processname="$1"

# check process running or not

if pgrep -x "$processname" > /dev/null
then
    echo "Process is running"
else
    echo "Process is not running"
fi