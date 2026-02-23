#!/bin/bash
useradd "$1"
echo "$1":"$1" | chpasswd

