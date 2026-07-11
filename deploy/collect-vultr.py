#!/usr/bin/env python3
import json, os, urllib.request
from datetime import datetime, timezone
for line in open('/etc/eaconsole/secrets.env',encoding='utf-8'):
    if line.strip() and not line.startswith('#') and '=' in line:
        k,v=line.strip().split('=',1); os.environ[k]=v
headers={'Authorization':f"Bearer {os.environ['VULTR_API_KEY']}"}
def get(path):
    req=urllib.request.Request('https://api.vultr.com/v2/'+path,headers=headers)
    with urllib.request.urlopen(req,timeout=20) as response: return json.load(response)
raw=get('instances')
account=get('account').get('account',{})
plans={p.get('id'):p for p in get('plans').get('plans',[])}
fields=('id','label','hostname','region','plan','os','ram','disk','vcpu_count','status','power_status','server_status','date_created')
instances=[]
for item in raw.get('instances',[]):
    instance={k:item.get(k) for k in fields}
    plan=plans.get(item.get('plan'),{})
    instance['monthly_cost']=plan.get('monthly_cost')
    instance['hourly_cost']=plan.get('hourly_cost')
    instances.append(instance)
billing={k:account.get(k) for k in ('balance','pending_charges','last_payment_date','last_payment_amount')}
billing['estimated_monthly_cost']=round(sum(float(x.get('monthly_cost') or 0) for x in instances),2)
payload={'generated_at':datetime.now(timezone.utc).isoformat(),'count':len(instances),'operational':sum(1 for x in instances if x.get('status')=='active' and x.get('power_status')=='running'),'billing':billing,'instances':instances}
target='/var/www/console.cm-ea.com/data/vultr.json'; tmp=target+'.tmp'
os.makedirs(os.path.dirname(target),exist_ok=True)
with open(tmp,'w',encoding='utf-8') as f: json.dump(payload,f,separators=(',',':'))
os.chmod(tmp,0o644); os.replace(tmp,target)
