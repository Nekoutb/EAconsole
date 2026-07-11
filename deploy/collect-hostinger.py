#!/usr/bin/env python3
import json, os, urllib.error, urllib.request
from datetime import datetime, timezone

for line in open('/etc/eaconsole/secrets.env',encoding='utf-8'):
    if line.strip() and not line.startswith('#') and '=' in line:
        k,v=line.strip().split('=',1); os.environ[k]=v
headers={'Authorization':f"Bearer {os.environ['HOSTINGER_API_TOKEN']}",'Accept':'application/json','User-Agent':'Hostinger-API-Client/EAConsole'}
def get(path):
    req=urllib.request.Request('https://developers.hostinger.com'+path,headers=headers)
    try:
        with urllib.request.urlopen(req,timeout=25) as response: return json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f'Hostinger API {exc.code}: {exc.read().decode("utf-8",errors="ignore")[:500]}')
def items(value):
    if isinstance(value,list): return value
    if isinstance(value,dict):
        for key in ('data','items','domains','subscriptions'):
            if isinstance(value.get(key),list): return value[key]
    return []
def first(obj,*keys):
    for key in keys:
        if obj.get(key) is not None:return obj.get(key)
    return None
portfolio=items(get('/api/domains/v1/portfolio'))
subscriptions=items(get('/api/billing/v1/subscriptions'))
now=datetime.now(timezone.utc)
domains=[]
for x in portfolio:
    expiry=first(x,'expires_at','expiration_date','expiresAt','expiry_date')
    days=None
    if expiry:
        try: days=(datetime.fromisoformat(str(expiry).replace('Z','+00:00')).date()-now.date()).days
        except Exception: pass
    domains.append({'domain':first(x,'domain','name'),'status':first(x,'status','state'),'created_at':first(x,'created_at','createdAt'),'expires_at':expiry,'days_remaining':days,'auto_renew':first(x,'auto_renew','auto_renewal','is_auto_renew_enabled'),'locked':first(x,'is_locked','domain_lock','locked')})
subs=[]
for x in subscriptions:
    price=first(x,'price','amount','renewal_price')
    subs.append({'name':first(x,'name','title','product_name'),'status':first(x,'status','state'),'started_at':first(x,'created_at','activated_at','starts_at'),'expires_at':first(x,'expires_at','expiration_date','ends_at'),'auto_renew':first(x,'auto_renew','auto_renewal','is_auto_renew_enabled'),'price_usd':round(float(price)/100,2) if price is not None else None,'currency':first(x,'currency','currency_code'),'billing_period':first(x,'billing_period','period')})
fx=600.0
try: fx=json.load(open('/var/www/console.cm-ea.com/data/vultr.json')).get('billing',{}).get('usd_to_xaf') or fx
except Exception: pass
dated=sorted((d for d in domains if d['days_remaining'] is not None),key=lambda d:d['days_remaining'])
payload={'generated_at':now.isoformat(),'domain_count':len(domains),'expiring_soon':sum(1 for d in domains if d['days_remaining'] is not None and d['days_remaining']<=30),'next_expiry':dated[0] if dated else None,'usd_to_xaf':fx,'domains':domains,'subscription_count':len(subs),'listed_value_usd':round(sum(s['price_usd'] or 0 for s in subs),2),'subscriptions':subs}
target='/var/www/console.cm-ea.com/data/hostinger.json'; tmp=target+'.tmp'
with open(tmp,'w',encoding='utf-8') as f: json.dump(payload,f,separators=(',',':'))
os.chmod(tmp,0o644); os.replace(tmp,target)
