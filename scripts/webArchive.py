import requests
import json

def WayBackMachine(url, domain):
    print('# Search for archived links on WBM:')
    headers = {
        'Host': 'web.archive.org',
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.101 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest'
    }

    params = (
        ('url', '{}'.format(url)),
        ('matchType', 'prefix'),
        ('collapse', 'urlkey'),
        ('output', 'json'),
        ('fl', 'original,mimetype,timestamp,endtimestamp,groupcount,uniqcount'),
        ('filter', '!statuscode:[45]..'),
    )

    response = requests.get('https://web.archive.org/web/timemap/', headers=headers, params=params, verify=False).text
    urlsList = []
    urls = json.loads(response)

    for url in urls:
        if 'text/html' in url[1]:
            urlsList.append(url[0])
    try:
        saveOutput = open('{}_Archived_links.txt'.format(domain), 'a')
        for link in urlsList:
            saveOutput.write(link + '\n')
        saveOutput.close()
    except:
        pass

    check = len(urlsList)
    if check > 1:
        print("- {} URLs have been captured for this domain, Results have been saved".format(len(urlsList)))
    else:
        print("- No URLs found on WBM")
