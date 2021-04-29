#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse, socket, sys
from scripts import header, extractLinks, subdomain, webArchive, result
import warnings; warnings.filterwarnings('ignore', message='Unverified HTTPS request')


print('# Pwnscan v0.1 | Coded by: StreghStreek GitHub.com/streghstreek')
parser = argparse.ArgumentParser(description="[*] PwnScan is an open source web application security scanner.")
parser.add_argument('-u', required=False, default=None, help='URL of the target site.')
parser.add_argument('-c', required=False, default=None, help='Use this to specify the cookies.')
args = vars(parser.parse_args())

if len(sys.argv) == 1:
    sys.exit("[!] Usage: python3 pwnscan.py -u https://example.com")

url = args['u']
getCookies = args['c']

if getCookies == None:
    cookies = None
else:
    cookies = {'Cookie': '{}'.format(getCookies)}

domain = url.split("//")[-1].split("/")[0].split('?')[0]
rmsub = '.'.join(domain.split('.')[-2:])
ipaddress = socket.gethostbyname(domain)
print('- Your target: {} ({})'.format(domain, ipaddress))


def main():
    try:
        header.hedaersCheck(url, cookies)
        extractLinks.getAll(domain, url, rmsub, cookies)
        webArchive.WayBackMachine(url, domain)
        subdomain.getSubdomains(domain)
        result.generate(domain, url, cookies)
        # Attack mood // Coming soon.
        #vulnScanner.gitRepo(url, cookies)
        #vulnScanner.xssScanner(domain)
        #vulnScanner.CRLFInjectionScanner(domain)

    except KeyboardInterrupt:
        exit('= Quitting!')

if __name__ == '__main__':
    main()
