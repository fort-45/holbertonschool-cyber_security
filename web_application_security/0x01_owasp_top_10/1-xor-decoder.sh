#!/bin/bash

# 1. Strip the {xor} prefix from the first argument
input="${1#\{xor\}}"

# 2. Decode Base64 and use a Python one-liner to XOR each byte with 95 (_)
echo "$input" | base64 -d | python3 -c "
import sys
# Read raw bytes from stdin
data = sys.stdin.buffer.read()
# XOR each byte with 95 and convert back to characters
decoded = ''.join(chr(b ^ 95) for b in data)
print(decoded, end='')
"
echo "" # Add a newline at the end to match the terminal output
