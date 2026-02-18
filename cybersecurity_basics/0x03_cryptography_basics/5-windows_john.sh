#!/bin/bash
john --format=nt --wordlist=/usr/share/wordlists/rockyou.txt "$1" && john --format=nt --show "$1" | awk -F: '{print $2}' > 5-password.txt
