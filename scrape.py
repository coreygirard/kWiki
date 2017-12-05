import requests
import re

def fetchPage(url):
    page = requests.get('http://en.wikipedia.org/wiki/'+url).text
    return page

def stripTags(page):
    return re.sub(r'<.*?>',r'',page)

def getBody(page):
    match = re.search(r'From Wikipedia, the free encyclopedia',page)
    start = match.end()
    end = len(page)

    for tag in [r'<a href="#See_also',
                r'<a href="#Notes_and_references',
                r'<a href="#Bibliography',
                r'<a href="#External_links']:
        match = re.search(tag,page)
        if match:
            end = min(end,match.start())

    return page[start:end]




def extractTitle(page):
    match = re.search(r'<h1 id="firstHeading" class="firstHeading" lang="en">(.*?)</h1>',page)
    return match.groups()[0]

def extractSummary(page):
    body = getBody(page)
    return stripTags(body[:re.search(r'<h2>',body).start()])

def extractBody(page):
    body = getBody(page)
    return stripTags(body)

def extractLinks(page):
    links = []
    for m in re.finditer(r'<a href="/wiki/(.*?)".*?title="(.*?)".*?>(.*?)</a>',page):
        a,b,c = m.groups()
        if ':' not in a:
            links.append({'url':a,'title':b,'text':c})
    return links









