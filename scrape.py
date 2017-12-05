import requests
import re

def fetchPage(url):
    '''
    >>> page = fetchPage('Logic')
    >>> type(page) == type('string')
    True
    >>> len(page) > 1000
    True
    '''

    page = requests.get('http://en.wikipedia.org/wiki/'+url).text
    return page

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

# get only text/HTML within <p></p> tags
def getParagraphs(page):
    temp = []
    for m in re.finditer(r'<p>(.*?)</p>',page):
        if m:
            temp.append(m.groups()[0])
            temp.append(' ')
    return (' '.join(temp)).strip()

def stripTags(page):
    '''
    >>> stripTags('counterfactuals, such as <i>If the moon is made of green cheese, then 2+2=5</i>, which are puzzling because natural language does not support the <a href="/wiki/Principle_of_explosion" title="Principle of explosion">principle of explosion</a>.')
    'counterfactuals, such as If the moon is made of green cheese, then 2+2=5, which are puzzling because natural language does not support the principle of explosion.'
    '''

    return re.sub(r'<.*?>',r'',page)

def stripBrackets(page):
    '''
    >>> stripBrackets('cannot be consistent and complete;[4] however,')
    'cannot be consistent and complete; however,'
    '''

    return re.sub(r'\[.*?\]',r'',page)

def stripCharacters(page):
    '''
    >>> stripCharacters('by means of "if&#160;... then&#160;...", due to')
    'by means of "if ;... then ;...", due to'
    '''

    page = re.sub(r'&#160',r' ',page)
    page = re.sub(r'[\t\n]',r' ',page)
    page = re.sub(r'[ ]+',r' ',page)
    return page

def cleanText(text):
    '''
    >>> cleanText('controversy in <a href="/wiki/Metaphysics" title="Metaphysics">metaphysics</a> on <a href="/wiki/Realism_versus_anti-realism" class="mw-redirect" title="Realism versus anti-realism">realism versus anti-realism</a>.</p> <h3><span class="mw-headline" id="Implication:_Strict_or_material">Implication: Strict or material</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/w/index.php?title=Logic&amp;action=edit&amp;section=21" title="Edit section: Implication: Strict or material">edit</a><span class="mw-editsection-bracket">]</span></span></h3><div role="note" class="hatnote navigation-not-searchable">')
    'controversy in metaphysics on realism versus anti-realism. Implication: Strict or material'
    '''

    text = stripCharacters(text)
    text = stripTags(text)
    text = stripBrackets(text)
    return text


def extractTitle(page):
    '''
    >>> t = '<h1 id="firstHeading" class="firstHeading" lang="en">Logic</h1>            <div id="bodyContent" class="mw-body-content">              <div id="siteSub" class="noprint">From Wikipedia, the free encyclopedia</div>'
    >>> extractTitle(t)
    'Logic'
    '''

    match = re.search(r'<h1 id="firstHeading" class="firstHeading" lang="en">(.*?)</h1>',page)
    return match.groups()[0]

def extractSummary(page):
    '''
    >>> with open('tests.html','r') as f:
    ...     page = f.read()
    >>> s = extractSummary(page)
    >>> s.startswith('Logic (from the Ancient Greek: ')
    True
    >>> s.endswith('studied in computer science, linguistics, psychology, and other fields.')
    True
    '''

    body = getBody(page)
    body = body[:re.search(r'<h2>',body).start()]

    body = getParagraphs(body)

    return cleanText(body)

def extractBody(page):
    '''
    >>> with open('tests.html','r') as f:
    ...     page = f.read()
    >>> body = extractBody(page)
    >>> body.startswith('Logic (from the Ancient Greek: λογική, translit. ;logikḗ), originally meaning "the word" or "what is spoken" (but coming to mean "thought" or "reason"), is generally held to consist of the systematic study of the form of valid inference.')
    True
    '''

    body = getBody(page)
    body = getParagraphs(body)
    return cleanText(body)

def extractLinks(page):
    '''
    >>> sample = ' of <a href="/wiki/Inference" title="Inference">inference</a>, including <a href="/wiki/Fallacies" class="mw-redirect" title="Fallacies">fallacies</a>, and the study of <a href="/wiki/Semantics" title="Semantics">semantics</a>, including <a href="/wiki/Paradox" title="Paradox">paradoxes</a>. Historically, logic has been studied in <a href="/wiki/Philosophy" title="Philosophy">philosophy</a> (since ancient times) and <a href="/wiki/Mathematics" title="Mathematics">mathematics</a> (since the mid-19th century), and recently logic has been studied in <a href="/wiki/Computer_science" title="Computer science">computer science</a>, <a href="/wiki/Linguistics" title="Linguistics">linguistics</a>, <a href="/wiki/Psychology" title="Psychology">psychology</a>, and other fields.</p>'
    >>> links = extractLinks(sample)
    >>> len(links)
    9
    >>> links[0] == {'title': 'Inference', 'url': 'Inference', 'text': 'inference'}
    True
    >>> links[1] == {'title': 'Fallacies', 'url': 'Fallacies', 'text': 'fallacies'}
    True
    >>> links[2] == {'title': 'Semantics', 'url': 'Semantics', 'text': 'semantics'}
    True
    >>> links[3] == {'title': 'Paradox', 'url': 'Paradox', 'text': 'paradoxes'}
    True
    >>> links[4] == {'title': 'Philosophy', 'url': 'Philosophy', 'text': 'philosophy'}
    True
    >>> links[5] == {'title': 'Mathematics', 'url': 'Mathematics', 'text': 'mathematics'}
    True
    >>> links[6] == {'title': 'Computer science', 'url': 'Computer_science', 'text': 'computer science'}
    True
    >>> links[7] == {'title': 'Linguistics', 'url': 'Linguistics', 'text': 'linguistics'}
    True
    >>> links[8] == {'title': 'Psychology', 'url': 'Psychology', 'text': 'psychology'}
    True
    '''

    links = []
    for m in re.finditer(r'<a href="/wiki/(.*?)".*?title="(.*?)".*?>(.*?)</a>',page):
        a,b,c = m.groups()
        if ':' not in a:
            links.append({'url':a,'title':b,'text':c})
    return links

def splitText(text):
    return re.split('[.!?]',text)







