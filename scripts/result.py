import requests, socket, os
from datetime import date

def generate(domain, url, cookies):
    today = date.today()
    template = open('scripts/template.html', 'r').read()
    if os.path.exists("Result/{}-{}-Result.html".format(today, domain)):
        os.remove("Result/{}-{}-Result.html".format(today, domain))

    resultFile = open("Result/{}-{}-Result.html".format(today, domain), "w")

    template = template.replace('*DOMAIN*', domain)

    # Summary
    ##Date
    template = template.replace('*DATE*', '{}'.format(today))

    ##Domain
    template = template.replace('*Domain*', domain)

    ##Server
    try:
        req = requests.get(url, verify=False, cookies=cookies).headers
        server = req['Server']
    except:
        server = 'None'
    template = template.replace('*SERVER*', server)

    ##IP
    ip = ipaddress = socket.gethostbyname(domain)
    template = template.replace('*IP*', ip)


    # Read output from all files:
    try:
        readFile = open('{}_Subdomains.txt'.format(domain), 'r').read().replace('\n', '<br>')
        template = template.replace('*Subdomains*', readFile)
        os.remove('{}_Subdomains.txt'.format(domain))
    except:
        template = template.replace('*ALL_URLs*', 'None')

    try:
        readFile = open('{}_All_URLs.txt'.format(domain), 'r').read().replace('\n', '<br>')
        template = template.replace('*ALL_URLs*', readFile)
        os.remove('{}_All_URLs.txt'.format(domain))
    except:
        template = template.replace('*ALL_URLs*', 'None')

    try:
        readFile = open('{}_URLs_with_parameters.txt'.format(domain), 'r').read().replace('\n', '<br>')
        template = template.replace('*URLs_with_parameters*', readFile)
        os.remove('{}_URLs_with_parameters.txt'.format(domain))
    except:
        template = template.replace('*URLs_with_parameters*', 'None')

    try:
        readFile = open('{}_Archived_links.txt'.format(domain), 'r').read().replace('\n', '<br>')
        template = template.replace('*Archived_URLs*', readFile)
        os.remove('{}_Archived_links.txt'.format(domain))
    except:
        template = template.replace('*Archived_URLs*', 'None')

    try:
        readFile = open('{}_URLs_from_JS.txt'.format(domain), 'r').read().replace('\n', '<br>')
        template = template.replace('*URLs_from_JS*', readFile)
        os.remove('{}_URLs_from_JS.txt'.format(domain))
    except:
        template = template.replace('*URLs_from_JS*', 'None')

    try:
        readFile = open('{}_Endpoints_from_JS.txt'.format(domain), 'r').read().replace('\n', '<br>')
        template = template.replace('*Endpoints_JS*', readFile)
        os.remove('{}_Endpoints_from_JS.txt'.format(domain))
    except:
        template = template.replace('*Endpoints_JS*', 'None')

    resultFile.write(template)
    resultFile.close()
    print('# Check Result folder.')
