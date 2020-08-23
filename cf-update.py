#!/usr/bin/env python
import platform
import requests
import socket
import sys
import CloudFlare

CFZONE = "27b6.com"

def get_current_ip():
    r = requests.get('http://myip.dnsomatic.com/')
    return r.text

def get_hostname():
    return platform.node()

def update_cloudflare(hostname):
    print("In update")
    params = {'name':CFZONE, 'per_page':1}
    cf = CloudFlare.CloudFlare()
    try:
#        print(params)
        zones = cf.zones.get(params=params)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones.get %d %s - api call failed' % (e, e))
    except Exception as e:
        exit('/zones - %s - api call failed' % (e))

    for zone in zones:
        zone_name = zone['name']
        zone_id = zone['id']
        print(zone_id, zone_name)
    return

def main():

    host = get_hostname()
    print("My hostname is {}".format(host))
    fqdn = host + "." + CFZONE
    print("My FQDN is {}".format(fqdn))
    ip = get_current_ip()
    print("I think my IP is {}".format(ip))
    try:
        dns_ip = socket.gethostbyname(fqdn) 
    except Exception as e:
        print(e)
        sys.exit(1)
    print("DNS thinks my IP is {}".format(dns_ip))
#    update_cloudflare(host)


    ip = "monkey"
    if ip == dns_ip:
        print("IP addresses match, no need to update")
        sys.exit(0)
    else:
        print("IP address mismatch, updating.")
        update_cloudflare(host)
    sys.exit(0)
if __name__ == '__main__':
    main()

