# kWiki

[![Build Status](https://travis-ci.org/coreygirard/kWiki.svg?branch=master)](https://travis-ci.org/coreygirard/kWiki) <br>
[![Codecov](https://img.shields.io/codecov/c/github/coreygirard/kWiki.svg)](https://codecov.io/gh/coreygirard/kWiki/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

### What

**kWiki** (pronounced _'quickie'_) aims to be a lightweight way to extract basic text from Wikipedia.
Zero dependencies! It can fetch a page's HTML and extract text and links.
If you want anything fancier, check out [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/).

### Why

Wikipedia is an incredibly useful resource with relatively reliable formatting,
but a few tricks are necessary to get at the good stuff. So I figured a modular minimalist parser
might be useful for myself and others.

### How

First, get the page's HTML via either a GET request or a download:

```python
import requests
page = requests.get('http://en.wikipedia.org/wiki/Software_testing').text
```

```python
with open('testing.html','r') as f:
    page = f.read()
```

**Note: if you are planning to parse more than a few files, use https://dumps.wikimedia.org/ instead of crawling.**

To get the page's title:

```python
title = scrape.extract_title(page)
print(title)
```

```
Software testing
```

To get the article 'summary' (loosely defined as the first chunk of the article, usually up until the 'Contents' box):

```python
summary = scrape.extract_summary(page)
print(summary)
```

```
Software testing is an investigation conducted to provide stakeholders with information about the
quality of the software product or service under test. ... ... In contrast, under an Agile approach,
requirements, programming, and testing are often done concurrently.
```

To get the entire text of the article (currently defined as all visible text not in boxes after the title and before any "See also", "References", "Notes and references", "Bibliography", "Further reading", or "External Links" sections:

```python
text = scrape.extract_text(page)
print(text)
```

```
Software testing is an investigation conducted to provide stakeholders with information about the
quality of the software product or service under test. ... ... By contrast, QA (quality assurance)
is the implementation of policies and procedures intended to prevent defects from reaching customers.
```

To get all links in the text of the article: (`text` is the text of the link itself, `title` is the text that appears on mouseover, and `url` is the destination)

```python
links = scrape.extract_links(page)
print(links)
```

```
[
 {'text': 'Software development',
  'title': 'Software development',
  'url': 'http://en.wikipedia.org/wiki/Software_development'},
 {'text': 'Processes',
  'title': 'Software development process',
  'url': 'http://en.wikipedia.org/wiki/Software_development_process'},
 {'text': 'Requirements',
  'title': 'Requirements analysis',
  'url': 'http://en.wikipedia.org/wiki/Requirements_analysis'},
 ...
 ...
 ...
]
```
