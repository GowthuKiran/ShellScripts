# Input: directory path → Output: top 5 largest files with size

#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <directory name>"
    exit 1
fi

# read direcory name
direcory="$1"

# check directory exits or not
if [ ! -d "$direcory" ]; then
    echo "Given directory is not exits"
    exit 1
fi

# Extract top 5 largest files
#cd $direcory && ls -lhs | sort -rh | head -n 5
find $directory  -maxdepth 1 -type f -exec du -h {} + | sort -rh | head -n 5


