import unittest
import doctest
import scrape

def setUpModule():
    global page
    with open('tests.txt','r') as f:
        page = f.read()

class TestFetch(unittest.TestCase):
    def test_fetch_page(self):
        self.assertEqual(scrape.makeUrl('Web_scraping'),'http://en.wikipedia.org/wiki/Web_scraping')

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        global page
        self.assertEqual(len(page),296351)

        title = scrape.extractTitle(page)

        self.assertEqual(title,'Logic')

class TestExtractLinks(unittest.TestCase):
    def test_extract_links(self):
        global page
        self.assertEqual(len(page),296351)

        links = scrape.extractLinks(page)

        self.assertEqual(len(links),948)

        self.assertEqual(links[10], {'text': 'Ethicists',
                                     'title': 'List of ethicists',
                                     'url': 'http://en.wikipedia.org/wiki/List_of_ethicists'})
        self.assertEqual(links[401], {'text': 'monotonicity of entailment',
                                      'title': 'Monotonicity of entailment',
                                      'url': 'http://en.wikipedia.org/wiki/Monotonicity_of_entailment'})

class TestExtractSummary(unittest.TestCase):
    def test_extract_summary(self):
        global page
        self.assertEqual(len(page),296351)

        summary = scrape.extractSummary(page)
        self.assertTrue(summary.startswith('Logic (from the Ancient Greek: '))
        self.assertTrue(summary.endswith('studied in computer science, linguistics, psychology, and other fields.'))

class TestExtractBody(unittest.TestCase):
    def test_extract_body(self):
        global page
        self.assertEqual(len(page),296351)

        body = scrape.extractText(page)
        self.assertTrue(body.startswith('Logic (from the Ancient Greek: '))
        self.assertTrue(body.endswith('with a view to shocking conventional readers" in his book A History of Western Philosophy.'))

class TestSplitIntoSentences(unittest.TestCase):
    def test_basic_split_sentences(self):
        text = 'A b c. D e f. G h i.'
        s = scrape.splitIntoSentences(text)
        self.assertEqual(s,['A b c.', 'D e f.', 'G h i.'])

        text = 'A b c! D e f! G h i!'
        s = scrape.splitIntoSentences(text)
        self.assertEqual(s,['A b c!', 'D e f!', 'G h i!'])

        text = 'A b c? D e f? G h i?'
        s = scrape.splitIntoSentences(text)
        self.assertEqual(s,['A b c?', 'D e f?', 'G h i?'])

        text = 'A b c. D e f? G h i!'
        s = scrape.splitIntoSentences(text)
        self.assertEqual(s,['A b c.', 'D e f?', 'G h i!'])

    def test_split_with_parentheses(self):
        text = 'Abc def. Ghi jkl. Mno pqr.'
        s = scrape.splitIntoSentences(text)
        self.assertEqual(s,['Abc def.', 'Ghi jkl.', 'Mno pqr.'])

        text = 'Abc def. (Ghi) jkl. Mno pqr.'
        s = scrape.splitIntoSentences(text)
        self.assertEqual(s,['Abc def.', '(Ghi) jkl.', 'Mno pqr.'])

        text = 'Abc def. Ghi (jkl). Mno pqr.'
        s = scrape.splitIntoSentences(text)
        self.assertEqual(s,['Abc def.', 'Ghi (jkl).', 'Mno pqr.'])

        text = 'Abc def. Ghi (jkl.) Mno pqr.'
        s = scrape.splitIntoSentences(text)
        self.assertEqual(s,['Abc def.', 'Ghi (jkl.)', 'Mno pqr.'])

        text = 'Abc def. Ghi (jkl) mno. Pqr.'
        s = scrape.splitIntoSentences(text)
        self.assertEqual(s,['Abc def.', 'Ghi (jkl) mno.', 'Pqr.'])

class TestSplitIntoWords(unittest.TestCase):
    def test_basic_split_words(self):
        text = 'A b c.'
        s = scrape.splitIntoWords(text)
        self.assertEqual(s,['A', 'b', 'c', '.'])

        text = 'A b c!'
        s = scrape.splitIntoWords(text)
        self.assertEqual(s,['A', 'b', 'c', '!'])

        text = 'A b c?'
        s = scrape.splitIntoWords(text)
        self.assertEqual(s,['A', 'b', 'c', '?'])

        text = 'Abc def ghi.'
        s = scrape.splitIntoWords(text)
        self.assertEqual(s,['Abc', 'def', 'ghi', '.'])

        text = 'Abc def ghi!'
        s = scrape.splitIntoWords(text)
        self.assertEqual(s,['Abc', 'def', 'ghi', '!'])

        text = 'Abc def ghi?'
        s = scrape.splitIntoWords(text)
        self.assertEqual(s,['Abc', 'def', 'ghi', '?'])

    def test_basic_split_with_parentheses(self):
        text = '(A b) c.'
        s = scrape.splitIntoWords(text)
        self.assertEqual(s,['(', 'A', 'b', ')', 'c', '.'])

        text = 'A (b) c.'
        s = scrape.splitIntoWords(text)
        self.assertEqual(s,['A', '(', 'b', ')', 'c', '.'])

        text = 'A (b c).'
        s = scrape.splitIntoWords(text)
        self.assertEqual(s,['A', '(', 'b', 'c', ')', '.'])

        text = 'A (b c.)'
        s = scrape.splitIntoWords(text)
        self.assertEqual(s,['A', '(', 'b', 'c', '.', ')'])



class TestSplitText(unittest.TestCase):
    def test_basic_split(self):
        text = 'A b c. D e f. G h i.'
        s = scrape.splitText(text)
        self.assertEqual(s,[['A', 'b', 'c', '.'], ['D', 'e', 'f', '.'], ['G', 'h', 'i', '.']])

        text = 'A b c! D e f! G h i!'
        s = scrape.splitText(text)
        self.assertEqual(s,[['A', 'b', 'c', '!'], ['D', 'e', 'f', '!'], ['G', 'h', 'i', '!']])

        text = 'A b c? D e f? G h i?'
        s = scrape.splitText(text)
        self.assertEqual(s,[['A', 'b', 'c', '?'], ['D', 'e', 'f', '?'], ['G', 'h', 'i', '?']])

        text = 'A b c. D e f! G h i?'
        s = scrape.splitText(text)
        self.assertEqual(s,[['A', 'b', 'c', '.'], ['D', 'e', 'f', '!'], ['G', 'h', 'i', '?']])

    def test_split_with_parentheses(self):
        text = 'A b c. (D e) f. G h i.'
        s = scrape.splitText(text)
        self.assertEqual(s,[['A', 'b', 'c', '.'],
                            ['(', 'D', 'e', ')', 'f', '.'],
                            ['G', 'h', 'i', '.']])

        text = 'A b c. D (e f.) G h i.'
        s = scrape.splitText(text)
        self.assertEqual(s,[['A', 'b', 'c', '.'],
                            ['D', '(', 'e', 'f', '.', ')'],
                            ['G', 'h', 'i', '.']])

    def test_split_real_text(self):
        global page
        self.assertEqual(len(page),296351)
        text = scrape.extractText(page)

        spl = scrape.splitText(text)
        self.assertEqual(spl[13],['It', 'is', 'necessary', 'because', 'indicative', 'sentences', 'of', 'ordinary', 'language', 'show', 'a', 'considerable', 'variety', 'of', 'form', 'and', 'complexity', 'that', 'makes', 'their', 'use', 'in', 'inference', 'impractical', '.'])
        self.assertEqual(spl[21],['The', 'concrete', 'terms', '"man"', ',', '"mortal"', ',', 'etc', '.', ',', 'are', 'analogous', 'to', 'the', 'substitution', 'values', 'of', 'the', 'schematic', 'placeholders', 'P', ',', 'Q', ',', 'R', ',', 'which', 'were', 'called', 'the', '"matter"', '(', 'Greek', 'hyle', ')', 'of', 'the', 'inference', '.'])



def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(scrape))
    return tests


if __name__ == '__main__':
    unittest.main()
