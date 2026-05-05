#!/bin/bash
awk '{print $12}' logs.txt | sort | uniq -c | sort -rn | head -1 | awk '{print $2}'
