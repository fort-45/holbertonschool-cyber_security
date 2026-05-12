#!/bin/bash
grep "Accepted password for root" auth.log | grep -oP 'from \K[\d.]+' | sort -u | wc -l
