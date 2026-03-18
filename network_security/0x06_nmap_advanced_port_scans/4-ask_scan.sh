#!/bin/bash
sudo nmap -sA -p "$2" --reason --host-timeot 1000ms "$1"
