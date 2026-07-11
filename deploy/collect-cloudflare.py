#!/usr/bin/env python3
import json, os, ssl, time, urllib.parse, urllib.request
from datetime import datetime, timezone

for line in open('/etc/eaconsole/secrets.env',encoding='utf-8'):
    if line.strip() and not line.startswith('#') and '=' in line:
        k,v=line.strip().split('=',1); os.environ[k]=v

headers={'Authorization':f"Bearer {os.environ['CLOUDFLARE_API_TOKEN']}",'Content-Type':'application/json'}
def cf(path):
    req=urllib.request.Request('https://api.cloudflare.com/client/v4/'+path,headers=headers)
    with urllib.request.urlopen(req,timeout=20) as response:
        body=json.load(response)
    if not body.get('success'): raise RuntimeError(body.get('errors'))
    return body.get('result')

zones=cf('zones?name=cm-ea.com')
if not zones: raise RuntimeError('cm-ea.com zone is not accessible with this token')
zone=zones[0]; zid=zone['id']
records=cf(f'zones/{zid}/dns_records?per_page=500')
try:
    ssl_mode=cf(f'zones/{zid}/settings/ssl').get('value')
except Exception:
    ssl_mode='permission unavailable'
names=sorted({r['name'] for r in records if r.get('type') in ('A','AAAA','CNAME') and '*' not in r.get('name','')})
websites=[]
for name in names:
    started=time.perf_counter(); status=None; error=None
    try:
        req=urllib.request.Request('https://'+name,headers={'User-Agent':'EAConsole-Monitor/1.0'})
        with urllib.request.urlopen(req,timeout=12,context=ssl.create_default_context()) as response: status=response.status
    except Exception as exc:
        status=getattr(exc,'code',None); error=type(exc).__name__
    latency=round((time.perf_counter()-started)*1000)
    websites.append({'name':name,'status':status,'operational':status is not None and status<500,'latency_ms':latency,'error':error})

payload={'generated_at':datetime.now(timezone.utc).isoformat(),'zone':{'name':zone.get('name'),'status':zone.get('status'),'paused':zone.get('paused'),'plan':(zone.get('plan') or {}).get('name'),'name_servers':zone.get('name_servers',[])},'ssl_mode':ssl_mode,'dns_record_count':len(records),'proxied_record_count':sum(1 for r in records if r.get('proxied')),'website_count':len(websites),'operational_websites':sum(1 for w in websites if w['operational']),'websites':websites}
target='/var/www/console.cm-ea.com/data/cloudflare.json'; tmp=target+'.tmp'
with open(tmp,'w',encoding='utf-8') as f: json.dump(payload,f,separators=(',',':'))
os.chmod(tmp,0o644); os.replace(tmp,target)
