#!/bin/bash
john --format=Raw-MD5 --wordlist=/usr/share/wordlists/rockyou.txt "$1" && john --format=Raw-MD5 --show "$1" | awk -F: '{print $2}' > 4-password.txt
