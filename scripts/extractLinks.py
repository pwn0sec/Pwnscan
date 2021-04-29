import requests
import mechanize
import os, re

def getAll(domain, url, rmsub, cookies):
    print('# Searching for links')
    def extractLinksAPI(domain):
        links = []
        linkWithParameter = []
        req = requests.get('https://api.hackertarget.com/pagelinks/?q={}'.format(domain)).text.splitlines()
        for url in req:
            if rmsub in url:
                if url not in links:
                    links.append(url)
                    try:
                        page, query = url.split('?')
                        paramsList = [pair.split('=') for pair in query.split('&')]
                        if url not in linkWithParameter:
                            linkWithParameter.append(url)
                    except:
                        pass

        if len(links) > 1:
            saveOutput = open('{}_All_URLs.txt'.format(domain), 'a')
            for link in links:
                saveOutput.write(link + '\n' )
            saveOutput.close()

        if len(linkWithParameter) > 1:
            saveOutput = open('{}_URLs_with_parameters.txt'.format(domain), 'a')
            for link in linkWithParameter:
                saveOutput.write(link + '\n' )
            saveOutput.close()


    def extractLinksFromHTML(url, cookies):
        try:
            domain = url.split("//")[-1].split("/")[0].split('?')[0]
            br = mechanize.Browser()
            br.set_handle_equiv(False)
            br.set_handle_robots(False)
            br.set_handle_referer(False)
            br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'), ('Accept', '*/*')]

            resp = br.open(url)
            urls = [link.absolute_url for link in br.links()]
            links = []
            linkWithParameter = []

            for link in urls:
                if domain in link:
                    if link not in links:
                        links.append(link)

                        try:
                            page, query = link.split('?')
                            paramsList = [pair.split('=') for pair in query.split('&')]
                            if link not in linkWithParameter:
                                linkWithParameter.append(link)
                        except:
                            pass

            if len(links) > 1:
                saveOutput = open('{}_All_URLs.txt'.format(domain), 'a')
                for link in links:
                    saveOutput.write(link+'\n')
                saveOutput.close()
            else:
                print('- No URL found')

            if len(linkWithParameter) > 1:
                saveOutput = open('{}_URLs_with_parameters.txt'.format(domain), 'a')
                for link in linkWithParameter:
                    saveOutput.write(link+'\n')
                saveOutput.close()
        except:
            pass

    def filterResults():
        files = ['{}_All_URLs.txt'.format(domain),
        '{}_URLs_with_parameters.txt'.format(domain)]
        try:
            for file in files:
                filter = []
                readFile = open(file, 'r')

                for line in readFile:
                    line = line.replace('\n', '')
                    if line not in filter:
                        filter.append(line)

                readFile.close()
                os.remove(file)
                saveOutput = open(file, 'a')

                for link in filter:
                    saveOutput.write(link + '\n')
                saveOutput.close()
        except:
            pass

        try:
            result = ['URLs found, Results have been saved', 'URLs with parameter found, Results have been saved']
            for file, output in zip(files, result):
                readFile = open(file, 'r').readlines()
                print('- {} {}'.format(len(readFile), output, file))
        except:
            pass

    def extractJsFiles(domain, url, cookies):
        print('# Searching for JS files')
        jsFiles = []
        req = requests.get(url, verify=False, cookies=cookies).text
        findJSfiles = re.findall('<script src="([^"]+)"', req)

        for file in findJSfiles:
            if not re.match('(?:http|https)://', file):
                jsFiles.append(('{}{}'.format(url, file)))
            else:
                if domain in file:
                    jsFiles.append(file)

        return jsFiles

    def extractUrl(domain, url, cookies):
        urls = extractJsFiles(domain, url, cookies)
        if len(urls) > 1:
            print('- {} JS files found, now I will search within these files to extract URLs and endpoints.'.format(len(urls)))
            urlsFilter = []
            endpointsList = []
            for url in urls:
                req = requests.get(url, verify=False, cookies=cookies).text
                jsFileOnWebsite = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', req)

                for data in jsFileOnWebsite:
                    if data not in urlsFilter:
                        urlsFilter.append(data)

                # Extract endpoints
                endpoints = re.findall(r'"([A-Za-z0-9_\./\\-]*)"', req)
                for endpoint in endpoints:
                    if '/' in endpoint:
                        if len(endpoint) > 2 and endpoint not in endpointsList:
                            endpointsList.append(endpoint)

            if len(endpointsList) > 1:
                saveOutput = open('{}_Endpoints_from_JS.txt'.format(domain), 'a')

                for endpoint in endpointsList:
                    saveOutput.write(endpoint + '\n')
                saveOutput.close()

            if len(urlsFilter) > 1:
                saveOutput = open('{}_URLs_from_JS.txt'.format(domain), 'a')

                for link in urlsFilter:
                    saveOutput.write(link + '\n')
                saveOutput.close()

            print('- I found {} URLs and {} endpoints from JS files.'.format(len(urlsFilter), len(endpointsList)))
        else:
            print('- JS files were not found.')
    extractLinksAPI(domain)
    extractLinksFromHTML(url, cookies)
    filterResults()
    extractUrl(domain, url, cookies)
