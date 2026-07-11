#!/usr/bin/env python3
import json, os, urllib.request
from datetime import datetime, timezone
for line in open('/etc/eaconsole/secrets.env',encoding='utf-8'):
    if line.strip() and not line.startswith('#') and '=' in line:
        k,v=line.strip().split('=',1); os.environ[k]=v
req=urllib.request.Request('https://api.vultr.com/v2/instances',headers={'Authorization':f"Bearer {os.environ['VULTR_API_KEY']}"})
with urllib.request.urlopen(req,timeout=20) as response: raw=json.load(response)
fields=('id','label','hostname','region','plan','os','ram','disk','vcpu_count','status','power_status','server_status','date_created')
instances=[{k:item.get(k) for k in fields} for item in raw.get('instances',[])]
payload={'generated_at':datetime.now(timezone.utc).isoformat(),'count':len(instances),'operational':sum(1 for x in instances if x.get('status')=='active' and x.get('power_status')=='running'),'instances':instances}
target='/var/www/console.cm-ea.com/data/vultr.json'; tmp=target+'.tmp'
os.makedirs(os.path.dirname(target),exist_ok=True)
with open(tmp,'w',encoding='utf-8') as f: json.dump(payload,f,separators=(',',':'))
os.chmod(tmp,0o644); os.replace(tmp,target)
