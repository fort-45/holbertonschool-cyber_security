#!/bin/bash
#!/bin/bash
whois "$1" | awk -F: '/^(Registrant|Admin|Tech)/{s=$1} /:/{gsub(/^[ \t]+/,"",$2); if($1~/(Street)/) printf "%s %s,%s \n",s,$1,$2; else if($1~/(Phone Ext)/) printf "%s %s:, %s\n",s,$1,$2; else printf "%s %s,%s\n",s,$1,$2}' > "$1.csv"
