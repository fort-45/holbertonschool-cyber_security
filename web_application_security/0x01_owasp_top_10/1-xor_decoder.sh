#!/bin/bash

# 1. Take the first argument and remove the "{xor}" prefix
encoded_string="${1#\{xor\}}"

# 2. Decode the Base64 string and XOR it with 95 (the '_' character)
# We use perl here because it's standard on Kali and handles the XORing smoothly
echo "$encoded_string" | base64 -d | perl -ne 'print $_ ^ "_" x length'
echo "" # Adds a newline to match the required output format
