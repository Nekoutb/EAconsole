#!/usr/bin/env python3
import json, os, urllib.error, urllib.request
from datetime import datetime, timezone

for line in open('/etc/eaconsole/secrets.env',encoding='utf-8'):
    if line.strip() and not line.startswith('#') and '=' in line:
        k,v=line.strip().split('=',1); os.environ[k]=v
req=urllib.request.Request('https://api.openai.com/v1/models',headers={'Authorization':f"Bearer {os.environ['OPENAI_API_KEY']}",'User-Agent':'EAConsole-Monitor/1.0'})
status='unavailable'; models=[]; error=None
try:
    with urllib.request.urlopen(req,timeout=20) as response:
        raw=json.load(response); models=[x.get('id') for x in raw.get('data',[]) if x.get('id')]
    status='operational'
except urllib.error.HTTPError as exc:
    error=f'HTTP {exc.code}'
except Exception as exc:
    error=type(exc).__name__
payload={'generated_at':datetime.now(timezone.utc).isoformat(),'api_status':status,'available_model_count':len(models),'key_type':'Project API key','billing_access':False,'usage_access':False,'subscription_status':'Pending billing details','error':error}
target='/var/www/console.cm-ea.com/data/openai.json'; tmp=target+'.tmp'
with open(tmp,'w',encoding='utf-8') as f: json.dump(payload,f,separators=(',',':'))
os.chmod(tmp,0o644); os.replace(tmp,target)
