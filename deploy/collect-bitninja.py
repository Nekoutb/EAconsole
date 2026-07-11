#!/usr/bin/env python3
import json, os, subprocess
from datetime import datetime, timezone

def active(service):
    return subprocess.run(['systemctl','is-active','--quiet',service]).returncode==0

services=['bitninja.service','bitninja-waf3.service','bitninja-process-analysis@false.service','bitninja-reliable-auto-update.service']
version=subprocess.run(['/usr/sbin/bitninjacli','--version'],capture_output=True,text=True,timeout=15).stdout.strip()
def pattern_count(filename,patterns):
    try:
        text=open('/var/log/bitninja/'+filename,encoding='utf-8',errors='ignore').read().lower()
        return sum(text.count(p) for p in patterns)
    except Exception: return 0
malware_events=pattern_count('mod.malware_detection.log',['infected','quarantined','malicious file','threat detected'])
blocked_events=pattern_count('mod.waf3.log',['blocked','attack'])+pattern_count('mod.ip_filter.log',['blocked','denied'])+pattern_count('mod.port_honeypot.log',['attack','blocked'])
agent_errors=pattern_count('error.log',['error','critical','fatal'])
fx=600.0
try:
    fx=json.load(open('/var/www/console.cm-ea.com/data/vultr.json',encoding='utf-8')).get('billing',{}).get('usd_to_xaf') or fx
except Exception: pass
now=datetime.now(timezone.utc); due=datetime(2026,7,16,tzinfo=timezone.utc)
service_states=[{'name':s.replace('.service',''),'active':active(s)} for s in services]
payload={'generated_at':now.isoformat(),'agent':{'installed':True,'version':version,'status':'active' if active('bitninja.service') else 'inactive','services':service_states},'activity':{'malware_events':malware_events,'blocked_events':blocked_events,'agent_errors':agent_errors,'healthy_services':sum(1 for s in service_states if s['active']),'risk_level':'attention' if agent_errors or malware_events or any(not s['active'] for s in service_states) else 'low','source':'Local BitNinja agent logs'},'billing':{'plan':'Free VPS (0–10 users)','server_name':'vultr','subscription_status':'Active','balance_usd':8,'upcoming_charge_usd':6,'amount_due_usd':0,'next_charge_date':due.isoformat(),'days_to_next_charge':max(0,(due.date()-now.date()).days),'usd_to_xaf':fx}}
target='/var/www/console.cm-ea.com/data/bitninja.json'; tmp=target+'.tmp'
with open(tmp,'w',encoding='utf-8') as f: json.dump(payload,f,separators=(',',':'))
os.chmod(tmp,0o644); os.replace(tmp,target)
