#!/usr/bin/env python3
import calendar, json, os, urllib.request
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
history=get('billing/history?per_page=500').get('billing_history',[])
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
try:
    fx=getattr(json.load(urllib.request.urlopen('https://open.er-api.com/v6/latest/USD',timeout=15)),'get')('rates',{}).get('XAF')
except Exception:
    fx=600.0
last_payment=abs(float(billing.get('last_payment_amount') or 0))
pending=float(billing.get('pending_charges') or 0)
projected=float(billing['estimated_monthly_cost'] or pending)
last_date=datetime.fromisoformat(billing['last_payment_date']) if billing.get('last_payment_date') else datetime.now(timezone.utc)
year=last_date.year+(1 if last_date.month==12 else 0); month=1 if last_date.month==12 else last_date.month+1
next_due=last_date.replace(year=year,month=month,day=min(last_date.day,calendar.monthrange(year,month)[1]))
billing.update({'currency':'XAF','usd_to_xaf':fx,'next_due_date':next_due.isoformat(),'days_to_next_payment':max(0,(next_due.date()-datetime.now(timezone.utc).date()).days),'estimated_next_payment':projected,'tracked_spend':round(last_payment+pending,2),'current_month_spend':round(pending,2),'projected_spend':round(projected,2)})
billing.update({'lifetime_spend':round(sum(float(x.get('amount') or 0) for x in history if x.get('type')=='invoice' and float(x.get('amount') or 0)>0),2),'invoice_count':sum(1 for x in history if x.get('type')=='invoice'),'payment_count':sum(1 for x in history if x.get('type')=='payment'),'history_start':min((x.get('date') for x in history if x.get('date')),default=None)})
payload={'generated_at':datetime.now(timezone.utc).isoformat(),'count':len(instances),'operational':sum(1 for x in instances if x.get('status')=='active' and x.get('power_status')=='running'),'billing':billing,'instances':instances}
target='/var/www/console.cm-ea.com/data/vultr.json'; tmp=target+'.tmp'
os.makedirs(os.path.dirname(target),exist_ok=True)
with open(tmp,'w',encoding='utf-8') as f: json.dump(payload,f,separators=(',',':'))
os.chmod(tmp,0o644); os.replace(tmp,target)
