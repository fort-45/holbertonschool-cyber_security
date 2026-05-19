#!/bin/bash
nmap -sV -A --script banners,ssl-enum-ciphers,default,smb-enum-domain $1 -oN service_enumeration_results.txt
