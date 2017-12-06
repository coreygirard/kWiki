# WikiScrape

### What

This package aims to be a lightweight way to extract basic text from Wikipedia.
Zero dependencies! It can fetch a page's HTML and extract text and links.
If you want anything fancier, check out [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/).


### Why

Wikipedia is an incredibly useful resource with relatively reliable formatting,
but a few tricks are necessary to get the text. So I figured a modular minimalist parser
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

**If you are planning to parse more than a few files, please use https://dumps.wikimedia.org/ instead of crawling.**

To get the page's title:
```python
title = scrape.extractTitle(page)
print(title)
```
```
Software testing
```

To get the article 'summary' (loosely defined as the first chunk of the article, usually up until the 'Contents' box:

```python
summary = scrape.extractSummary(page)
print(summary)
```
```
Software testing is an investigation conducted to provide stakeholders with information about the quality of the software product or service under test. ... ... In contrast, under an Agile approach, requirements, programming, and testing are often done concurrently.
```

To get the entire text of the article (currently defined as all visible text not in boxes after the title and before any "See also", "References", "Notes and references", "Bibliography", "Further reading", or "External Links" sections:

```python
text = scrape.extractText(page)
print(text)
```
```
Software testing is an investigation conducted to provide stakeholders with information about the quality of the software product or service under test. ... ... By contrast, QA (quality assurance) is the implementation of policies and procedures intended to prevent defects from reaching customers.
```

To get all links in the text of the article: ('text' is the text of the link itself, 'title' is the text that appears on mouseover, and 'url' is the destination)

```python
links = scrape.extractLinks(page)
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







# Swarm

## Ranges

#### Operations

**Creating**

Range notation in Swarm is a more compact way of specifying lists that are composed of integers and follow a linear pattern.
`[a:b:c]` is the canonical form, but many variations exist. This form defines a sequence that starts with `a`, steps by `b`, and ends with a value `n` where `n <= c`. Examples:
- `[0:1:8]` is equivalent to `[0,1,2,3,4,5,6,7,8]`
- `[0:1:0]` is equivalent to `[0]`
- `[0:2:6]` is equivalent to `[0,2,4,6]`
- `[0:2:5]` is equivalent to `[0,2,4]`
- `[6:-2:-4]` is equivalent to `[6,4,2,0,-2,-4]`

`b` can be omitted (`[a:c]`), and defaults to `1` if `a < c` or `-1` if `a > c`.
If `a == c`, `[a:b:c]` returns `[a]` no matter the value or existence of `b`.

Additionally, either `[` or `]` may be exchanged for the corresponding parenthesis, which makes that bound exclusive rather than inclusive. For example:

- `[4:7]` = `[4,5,6,7]`
- `[4:7)` = `[4,5,6]`
- `(4:7]` = `[5,6,7]`
- `(4:7)` = `[5,6]`

The same applies where `b != 1`:
- `(4:2:8)` = `[6]`
- `(0:3:12]` = `[3,6,9,12]`
`(` works by simply skipping what would have been the first element if `[` had been used.
`)` works by ensuring that the final element in the sequence is less than `c`

If `a == c` and one or both bounds are exclusive, an empty array is the result:
- `[5:b:5]` = `[5]` for any `b`
- `[5:b:5)` = `[]` for any `b`
- `(5:b:5]` = `[]` for any `b`
- `(5:b:5)` = `[]` for any `b`

#### Properties

- **`.length`** Returns the number of elements in the range

#### Methods

- **`a.overlap(b)`** Returns a new `Range` that contains only the elements in both `a` and `b`.
`[1:7].overlap([4:9])` = `[4:7]`
`[1:2:7].overlap([4:2:9])` = `[]`

- **`.normalize()`** Converts the `Range`, in-place, to a normalized form, ie inclusive on both ends, and with `a` and `c` as close as possible.
`(4:8).normalize()` = `[5:7]`
`(6:2].normalize()` = `[5:2]`
`(0:3:14].normalize()` = `[3:3:12]`
`(-2:-5:-105]` = `[-7:-5:-102]`




