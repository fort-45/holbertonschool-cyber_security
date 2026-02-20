#!/bin/bash
hashcat -a 1 "$1" "$1" --stdout
