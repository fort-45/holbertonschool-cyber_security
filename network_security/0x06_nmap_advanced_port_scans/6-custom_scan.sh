#!/bin/bash
sudo nmap -scanflag URGACKPSHRSTSYNFIN -p "$2" "$1" -oN custom_scan.txt &> /dev/null
