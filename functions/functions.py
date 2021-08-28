"""
Collect the functions used in the notebook to make the display cleaner
"""
# imports
import pandas as pd
import numpy as np

# Viz imports
import matplotlib.pyplot as plt
import seaborn as sns

# turn off warnings
import warnings
warnings.filterwarnings('ignore')

import csv
import json
import datetime as datetime
import time

# ip/AS lookup tools
import socket
from ipwhois import IPWhois
from ipwhois.net import Net
from ipwhois.asn import IPASN


def iplookup(ipaddress):
    try: 
        fullhostname = socket.gethostbyaddr(ipaddress)
        hostname = fullhostname[0]
    except Exception as e:
        hostname = ipaddress
    return hostname


def getAsInfo(item, category='asn', **kwargs):
    """
    We want to do a lookup on the non-rfc1918 address either send or receive in one fell swoop
    
    df[['Source IP','Destination IP']].apply(getAsInfoKwargs, category='asncidr',axis=1)
    
    asncidr, asn, asn_desc, asn_country
    """
    one, two = item['Source IP'], item['Destination IP']
    target_ip = one
    
    private = ['10.','172.','192.168.']
    
    # get as info for the non-rfc1918 address
    if '192.168' in one:
        target_ip = two
    
    net = Net(target_ip)
    obj = IPASN(net)
    results = obj.lookup()
    
    if category == 'reg':
        return results['asn_registry']
    elif category == 'asn':
        return results['asn']
    elif category == 'asn_cidr':
        return results['asn_cidr']
    elif category == 'asn_country':
        return results['asn_country_code']
    elif category == 'asn_date':
        return results['asn_date']
    elif category == 'asn_desc':
        return results['asn_description']
    if category == 'all':
        return results['asn_cidr'], results['asn'], results['asn_description'],results['asn_country_code']
    else:
        return False
    

def is_sketchy(asn):
    sketchy_countries = ['CN','RU','VN','HK','TW','IN','BR','RO','HU','KR','IT','UG','TR','MY','BO','CO']
    return True if asn in sketchy_countries else False 

def is_corp(asn):
    invasive_corps = ['AMAZON','APPLE','GOOGLE','MICROSOFT','CLOUDFLARENET','SALESFORCE','AKAMAI','OPENDNS']
    return True if asn in invasive_corps else False

def is_sketchy_provider(asn):
     sketchy_providers = []
     providers = open('records/beaconish_asns','r').readlines()
     for p in providers:
            sketchy_providers.append(p.split()[0])
     return True if asn in sketchy_providers else False

def isip(id):
    """
    is the string an ipv4 address?
    """
    try: 
        socket.inet_aton(id)
        return True
    except:
        return False


def has_dns(id):
    """
    earlier we checked for a dns entry and return an IP if none is found.
    here we say "if that id is an IP then there was no DNS record"
    """
    try: 
        socket.inet_aton(id)
        return False
    except:
        return True

def has_ptr(id):
    """
    earlier we checked for a ptr and return an IP if none is found.
    here we say "if that id is an IP then there was no PTR record"
    """
    try: 
        socket.inet_aton(id)
        return False
    except:
        return True


def f2b_marked(s):
    """
    fail2ban responds to connection overload by replying with ICMP type 3 "unreachable"
    if this exists in the connection, we'll presume that this host was flooding
    """
    if 'icmp' in s:
        return True
    return False

def in_blacklist(ip):
    blacklistraw = open('records/20210827154850_blacklisted_ips.txt','r').readlines()
    blacklist = [x.strip('\n') for x in blacklistraw]
    if ip not in blacklist:
        return False
    return True


def tally_total(item):
    """
    tally up scores per row. 
    where are we **sending** data (beacons)?
    need the columns
    df[['Score','asn',sketchy','src_ptr','dst_ptr','iscorp','sketchy_provider','src_dns','dst_dns','fail2ban','blacklisted']]

    must call apply with axis=1 e.g.
    df[['Score','asn','sketchy','src_ptr','dst_ptr','iscorp','sketchy_provider','src_dns','dst_dns','fail2ban','blacklisted']].apply(test_return,axis=1)
    """

    total=item['bscore']
    
    # presuming our internal network is in RFC1918. Open Internet Addresses should have reverse pointers and DNS, even if we don't internally
    if item['asn'] == 'rfc1918':
        if not item['src_ptr']:
            total +=2
        elif not item['src_dns']:
            total +=2
    elif item['asn'] != 'rfc1918':
        if not item['dst_ptr']:
            total +=2
        elif not item['dst_dns']:
            total +=2
    # fail2ban violations are from 
    if item['fail2ban'] :
        total +=3
    # is the connection to a sketchy country?
    elif item['sketchy']:
        total+=3
    # how about to a sketchy provider?
    elif item['sketchy_provider']:
        total +=3
    # is the IP in the spamhaus blacklist?
    elif item['blacklisted']:
        total +=3
    # corporate spyware is the lowest priority. This scoring should make it easier to build filters, also.
    elif item['iscorp']:
        total +=1
    return total
        


def total_score(row):
    """
    multiply RITA score and bscore
    Usage:
    df[['Score','bscore']].apply(total_score,axis=1)
    """
    return row['Score'] * row['bscore']



