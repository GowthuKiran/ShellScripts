# This script is to create backup folder and copy files into it
# Author: KiranKumar Chintha
# Date: 15-08-25
# Version: v1

#!/bin/bash
# check file exits or not
if [ ! -z "$1" ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

# read file
file="$1"

# check file exits are not
if [ ! -f  "$file"]; then
    echo "file doesn't exit"
    exit 1
fi

# Create backup directory if not exits
backup_dir="backup"
makdir -p $backup_dir

# Extract timestamp
time_stamp=$(date +"%y%m%d_%H%M%S")

# extract file name
filename=$(basename "$file")

# Final backup file name
backup_file="$backup_dir/${filename}_$time_stamp"

# copy file to backup folder
cp $file $backup_file

# Display backup status
if [ ! -f "$backup_file"]; then
    echo "file not copied Successfully"
else
    echo "Backup of given file is completed successfully"
fi