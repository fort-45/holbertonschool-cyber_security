#!/bin/bash
hashcat -m 0 "$1" -a 1 wordlist1.txt wordlist2.txt && hashcat -m 0 "$1" --show | cut -d: -f2 > 9-password.txt
