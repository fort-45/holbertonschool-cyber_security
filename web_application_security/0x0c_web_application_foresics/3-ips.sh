#!/bin/bash
grep "Accepted password" auth.log | grep -oP 'from \K[\d.]+' | sort -u | wc -l
