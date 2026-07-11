#!/usr/bin/env python3
from pathlib import Path

block = '''
    <Location "/">
        AuthType Basic
        AuthName "Elite Advisors IT Operations"
        AuthUserFile /etc/eaconsole/.htpasswd
        Require valid-user
    </Location>
'''

for name in ('console.cm-ea.com.conf', 'console.cm-ea.com-le-ssl.conf'):
    path = Path('/etc/apache2/sites-available') / name
    text = path.read_text()
    if 'AuthUserFile /etc/eaconsole/.htpasswd' not in text:
        text = text.replace('</VirtualHost>', block + '</VirtualHost>')
        path.write_text(text)
