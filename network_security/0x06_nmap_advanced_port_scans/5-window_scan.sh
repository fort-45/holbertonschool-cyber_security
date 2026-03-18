#!/bin/bash
sudo nmap -sW -p "$2" --exclude-port "$3" "$1"
