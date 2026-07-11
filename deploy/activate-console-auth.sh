#!/usr/bin/env bash
set -euo pipefail
password="$(openssl rand -base64 24 | tr -d '/+=' | head -c 22)"
htpasswd -bcB /etc/eaconsole/.htpasswd eaadmin "$password" >/dev/null
chmod 640 /etc/eaconsole/.htpasswd
chown root:www-data /etc/eaconsole/.htpasswd
python3 /tmp/enable-console-auth.py
apache2ctl configtest
systemctl reload apache2
unauth="$(curl -sS -o /dev/null -w '%{http_code}' -H 'Host: console.cm-ea.com' https://127.0.0.1/ -k)"
auth="$(curl -sS -o /dev/null -w '%{http_code}' -u "eaadmin:$password" -H 'Host: console.cm-ea.com' https://127.0.0.1/ -k)"
printf 'LOGIN_USERNAME=eaadmin\nLOGIN_PASSWORD=%s\nUNAUTHENTICATED_HTTP=%s\nAUTHENTICATED_HTTP=%s\n' "$password" "$unauth" "$auth"
