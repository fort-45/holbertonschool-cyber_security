#!/bin/bash
grep "^smtpd_tls_security_level" /etc/posfix/main.cf || echo "STARTTLS not configured"
