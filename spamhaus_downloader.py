#!/usr/bin/env python
"""

This downloads the latest spam list from spamhaus, unzips it, then extracts ip addresses and domains.
Results are saved into a file called:
<datestamp>_blacklist.txt


https://urlhaus.abuse.ch/downloads/csv/
"""

from datetime import datetime
import os, csv, re
import urllib.request
import zipfile
from io import BytesIO

DATE=datetime.now().strftime('%Y%m%d%H%M%S')
encoding = 'utf-8'
pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')


# conversion functions
def isip(item):
     pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
     return pattern.search(item)[0]

def isdomain(item):
    chunks = item.split('/')
    return chunks[2]



# download zipfile, unzip into an array of bytes-like objects:
with urllib.request.urlopen('https://urlhaus.abuse.ch/downloads/csv/') as f:
    zipdata =  BytesIO(f.read())
    blacklistzip= zipfile.ZipFile(zipdata)
# the file inside is called 'csv.txt'
blacklistarr = blacklistzip.open('csv.txt').readlines()


# digest the output into ip addresses and domains
stash_ips = []
stash_domains = []

for b in blacklistarr:
    line = b.decode(encoding)
    if len(line) > 100:
        if pattern.search(line):
            stash_ips.append(isip(line))
        else:
            stash_domains.append(isdomain(line))
# eliminate dupes
domains = [x for x in set(stash_domains)]
ips  = [x for x in set(stash_ips)]


# write out to files
domainsfile=f'{DATE}_blacklisted_domains.txt'
ipsfile=f'{DATE}_blacklisted_ips.txt'
#
with open(domainsfile,'w') as f:
    for x in stash_domains:
        mystr=f'{x}\n'
        f.write(mystr)
f.close()


with open(ipsfile,'w') as f:
    for x in stash_ips:
        mystr=f'{x}\n'
        f.write(mystr)
f.close()


