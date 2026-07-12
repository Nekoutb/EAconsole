#!/usr/bin/env python3
import json, os, urllib.error, urllib.request
from datetime import datetime, timezone

for line in open('/etc/eaconsole/secrets.env',encoding='utf-8'):
    if line.strip() and not line.startswith('#') and '=' in line:
        k,v=line.strip().split('=',1); os.environ[k]=v.strip('"')
headers={'Authorization':f"Bearer {os.environ['MAILERSEND_API_KEY']}",'Accept':'application/json','User-Agent':'EAConsole-Monitor/1.0'}
def get(path):
    req=urllib.request.Request('https://api.mailersend.com/v1/'+path,headers=headers)
    with urllib.request.urlopen(req,timeout=20) as response: return json.load(response)
errors=[]
try: domains_raw=get('domains?limit=100').get('data',[])
except Exception as exc: domains_raw=[]; errors.append('domains:'+type(exc).__name__)
try: quota=get('api-quota')
except Exception as exc: quota={}; errors.append('quota:'+type(exc).__name__)
try: messages_raw=get('messages?limit=100').get('data',[])
except Exception as exc: messages_raw=[]; errors.append('messages:'+type(exc).__name__)
domains=[{'name':d.get('name'),'verified':bool(d.get('is_verified')),'id':d.get('id')} for d in domains_raw]
statuses={}
for m in messages_raw:
    status=(m.get('status') or 'unknown').lower(); statuses[status]=statuses.get(status,0)+1
limit=quota.get('limit') or quota.get('quota') or quota.get('daily_limit')
remaining=quota.get('remaining') or quota.get('remaining_requests')
plan={100:'Trial',1000:'Hobby',100000:'Starter',500000:'Professional / Enterprise'}.get(limit,'Not exposed')
payload={'generated_at':datetime.now(timezone.utc).isoformat(),'api_status':'operational' if domains_raw and not errors else ('partial' if domains_raw else 'unavailable'),'domain_count':len(domains),'verified_domains':sum(1 for d in domains if d['verified']),'domains':domains,'message_count_visible':len(messages_raw),'message_statuses':statuses,'quota':{'daily_limit':limit,'remaining':remaining,'plan_inferred':plan},'billing':{'lifetime_spend':None,'current_spend':None,'next_payment_date':None,'note':'MailerSend API does not expose invoice or subscription payment history.'},'errors':errors}
target='/var/www/console.cm-ea.com/data/mailersend.json'; tmp=target+'.tmp'
with open(tmp,'w',encoding='utf-8') as f: json.dump(payload,f,separators=(',',':'))
os.chmod(tmp,0o644); os.replace(tmp,target)
