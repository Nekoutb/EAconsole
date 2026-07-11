#!/usr/bin/env bash
set -euo pipefail
set -a
. /etc/eaconsole/secrets.env
set +a
code="$(curl -sS -o /tmp/eaconsole-vultr-check.json -w '%{http_code}' -H "Authorization: Bearer ${VULTR_API_KEY}" https://api.vultr.com/v2/instances)"
unset VULTR_API_KEY
if [ "$code" != "200" ]; then
  echo "Vultr API validation failed: HTTP $code"
  rm -f /tmp/eaconsole-vultr-check.json
  exit 1
fi
python3 -c 'import json; d=json.load(open("/tmp/eaconsole-vultr-check.json")); print("Vultr API verified; instances=" + str(len(d.get("instances", []))))'
rm -f /tmp/eaconsole-vultr-check.json
