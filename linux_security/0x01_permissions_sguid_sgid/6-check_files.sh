#!/bin/bash
find "$1" -mntime -1 -perm -6000 -type f -exec ls -l {} \;
