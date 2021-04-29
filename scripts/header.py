import requests


def hedaersCheck(url, cookies):
    def getServer(url, cookies):
        try:
            req = requests.get(url, verify=False, cookies=cookies).headers
            print("- Server: " + req['Server'])
        except:
            pass

    def httpMethods(url, cookies):
        try:
            req = requests.options(url, verify=False, cookies=cookies).headers
            if req['Allow'] == '':
                pass
            else:
                print('- HTTP methods: ' + req['Allow'])
        except:
            pass

    def checkCSP(url, cookies):
        try:
            req = requests.get(url, verify=False, cookies=cookies).headers
            if 'Content-Security-Policy' in req:
                pass
            else:
                print("- Content Security Policy (CSP) not implemented")
        except:
            pass

    def checkClickjacking(url, cookies):
        try:
            req = requests.get(url, verify=False, cookies=cookies).headers
            if 'X-Frame-Options' in req:
                pass
            else:
                print("- Clickjacking: X-Frame-Options header missing")
        except:
            pass

    def checkMissingXSSProtection(url, cookies):
        try:
            req = requests.get(url, verify=False, cookies=cookies).headers
            if 'X-XSS-Protection' in req:
                pass
            else:
                print("- X-XSS-Protection header missing")
        except:
            pass

    def checkCORS(url, cookies):
        try:
            req = requests.get(url, headers={"Origin":"https://evil.com"}, verify=False, cookies=cookies).headers
            if req['Access-Control-Allow-Origin'] == "https://evil.com":
                print("- Cross-origin Resource Sharing (CORS) misconfiguration")
        except:
            pass

    def hostHeaderAttack(url, cookies):
        try:
            req = requests.get(url, headers={'Host': 'evil.com'}, verify=False, allow_redirects=False, cookies=cookies).headers
            if "evil.com" in req['Location']:
                print("- Vulnerable to Host header attack: curl -i -s -k -X 'GET' -H 'Host: evil.com' '{}'".format(url))
        except:
            pass

    getServer(url, cookies)
    httpMethods(url, cookies)
    checkCSP(url, cookies)
    checkClickjacking(url, cookies)
    checkMissingXSSProtection(url, cookies)
    checkCORS(url, cookies)
    hostHeaderAttack(url, cookies)
