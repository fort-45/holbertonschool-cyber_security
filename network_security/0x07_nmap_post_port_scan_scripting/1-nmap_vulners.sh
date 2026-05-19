#!/bin/bash
nmap --script nmap-vulners/ -p 80,443 "$1"
