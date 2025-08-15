# This script is to pass directory as an input and retrun the files count as output
# Author: KiranKumar Chintha

#!/bin/bash

# If argument not passed
if [ ! -z "$1" ]; then
    echo "Usage: $0 <Directory name>"
    exit 1
fi

# read directory
directory="$1"

# check number of files
number_of_files="cd $directory && ls -l | grep -v "^total" | wc -l"

if [ "$number_of_files">0]; then
    echo "Number of files in the given directory are: $(number_of_files)"
else
    echo "There are no files in the given directory"

#############################################################################################

# # count only files (not directories)
# file_count=$(find "$directory" -maxdepth 1 -type f | wc -l)

# # count only directories (excluding the directory itself)
# dir_count=$(find "$directory" -maxdepth 1 -type d | wc -l)
# dir_count=$((dir_count - 1))