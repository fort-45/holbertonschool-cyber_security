#!/bin/bash
nmap --open -sX -p 440-450 --reason --packet-trace "$1"
