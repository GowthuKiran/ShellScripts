#!/bin/bash

# Script to count occurrences of a specific character in a file or string

echo "Enter the character to search:"
read char

echo "Choose input type:"
echo "1. From a file"
echo "2. From a string"
read choice

if [ "$choice" -eq 1 ]; then
    echo "Enter file name:"
    read filename

    if [ -f "$filename" ]; then
        count=$(grep -o "$char" "$filename" | wc -l)
        echo "The character '$char' occurred $count times in file '$filename'."
    else
        echo "File not found!"
    fi

elif [ "$choice" -eq 2 ]; then
    echo "Enter the string:"
    read input_string

    count=$(echo "$input_string" | grep -o "$char" | wc -l)
    echo "The character '$char' occurred $count times in the given string."

else
    echo "Invalid choice!"
fi
