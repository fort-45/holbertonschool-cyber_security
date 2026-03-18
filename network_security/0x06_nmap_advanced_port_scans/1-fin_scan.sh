#!/bin/bash
sudo nmap -p 80-85 -sF -f -T2 "$1"
