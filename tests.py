import unittest
import doctest
import scrape

with open('tests.txt', 'r') as f:
    page = f.read()

class TestFetch(unittest.TestCase):
    def test_fetch_page(self):
        self.assertEqual(scrape.make_url('Web_scraping'),
                         'http://en.wikipedia.org/wiki/Web_scraping')

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(len(page), 296351)

        title = scrape.extract_title(page)

        self.assertEqual(title, 'Logic')

class TestExtractLinks(unittest.TestCase):
    def test_extract_links(self):
        self.assertEqual(len(page), 296351)

        links = scrape.extract_links(page)

        self.assertEqual(len(links), 948)

        self.assertEqual(links[10], {'text': 'Ethicists',
                                     'title': 'List of ethicists',
                                     'url': 'http://en.wikipedia.org/wiki/'
                                            'List_of_ethicists'})
        self.assertEqual(links[401], {'text': 'monotonicity of entailment',
                                      'title': 'Monotonicity of entailment',
                                      'url': 'http://en.wikipedia.org/wiki/'
                                             'Monotonicity_of_entailment'})

class TestExtractSummary(unittest.TestCase):
    def test_extract_summary(self):
        self.assertEqual(len(page), 296351)

        summary = scrape.extract_summary(page)

        expected_prefix = 'Logic (from the Ancient Greek: '
        self.assertTrue(summary.startswith(expected_prefix))


        expected_suffix = 'studied in computer science, linguistics, ' + \
                          'psychology, and other fields.'
        self.assertTrue(summary.endswith(expected_suffix))

class TestExtractBody(unittest.TestCase):
    def test_extract_body(self):
        self.assertEqual(len(page), 296351)

        body = scrape.extract_text(page)
        self.assertTrue(body.startswith('Logic (from the Ancient Greek: '))
        self.assertTrue(body.endswith('with a view to shocking conventional '
            'readers" in his book A History of Western Philosophy.'))

class TestSplitIntoSentences(unittest.TestCase):
    def test_basic_split_sentences(self):
        text = 'A b c. D e f. G h i.'
        s = scrape.split_into_sentences(text)
        self.assertEqual(s, ['A b c.', 'D e f.', 'G h i.'])

        text = 'A b c! D e f! G h i!'
        s = scrape.split_into_sentences(text)
        self.assertEqual(s, ['A b c!', 'D e f!', 'G h i!'])

        text = 'A b c? D e f? G h i?'
        s = scrape.split_into_sentences(text)
        self.assertEqual(s, ['A b c?', 'D e f?', 'G h i?'])

        text = 'A b c. D e f? G h i!'
        s = scrape.split_into_sentences(text)
        self.assertEqual(s, ['A b c.', 'D e f?', 'G h i!'])

    def test_split_with_parentheses(self):
        text = 'Abc def. Ghi jkl. Mno pqr.'
        s = scrape.split_into_sentences(text)
        self.assertEqual(s, ['Abc def.', 'Ghi jkl.', 'Mno pqr.'])

        text = 'Abc def. (Ghi) jkl. Mno pqr.'
        s = scrape.split_into_sentences(text)
        self.assertEqual(s, ['Abc def.', '(Ghi) jkl.', 'Mno pqr.'])

        text = 'Abc def. Ghi (jkl). Mno pqr.'
        s = scrape.split_into_sentences(text)
        self.assertEqual(s, ['Abc def.', 'Ghi (jkl).', 'Mno pqr.'])

        text = 'Abc def. Ghi (jkl.) Mno pqr.'
        s = scrape.split_into_sentences(text)
        self.assertEqual(s, ['Abc def.', 'Ghi (jkl.)', 'Mno pqr.'])

        text = 'Abc def. Ghi (jkl) mno. Pqr.'
        s = scrape.split_into_sentences(text)
        self.assertEqual(s, ['Abc def.', 'Ghi (jkl) mno.', 'Pqr.'])

class TestSplitIntoWords(unittest.TestCase):
    def test_basic_split_words(self):
        text = 'A b c.'
        s = scrape.split_into_words(text)
        self.assertEqual(s, ['A', 'b', 'c', '.'])

        text = 'A b c!'
        s = scrape.split_into_words(text)
        self.assertEqual(s, ['A', 'b', 'c', '!'])

        text = 'A b c?'
        s = scrape.split_into_words(text)
        self.assertEqual(s, ['A', 'b', 'c', '?'])

        text = 'Abc def ghi.'
        s = scrape.split_into_words(text)
        self.assertEqual(s, ['Abc', 'def', 'ghi', '.'])

        text = 'Abc def ghi!'
        s = scrape.split_into_words(text)
        self.assertEqual(s, ['Abc', 'def', 'ghi', '!'])

        text = 'Abc def ghi?'
        s = scrape.split_into_words(text)
        self.assertEqual(s, ['Abc', 'def', 'ghi', '?'])

    def test_basic_split_with_parentheses(self):
        text = '(A b) c.'
        s = scrape.split_into_words(text)
        self.assertEqual(s, ['(', 'A', 'b', ')', 'c', '.'])

        text = 'A (b) c.'
        s = scrape.split_into_words(text)
        self.assertEqual(s, ['A', '(', 'b', ')', 'c', '.'])

        text = 'A (b c).'
        s = scrape.split_into_words(text)
        self.assertEqual(s, ['A', '(', 'b', 'c', ')', '.'])

        text = 'A (b c.)'
        s = scrape.split_into_words(text)
        self.assertEqual(s, ['A', '(', 'b', 'c', '.', ')'])



class TestSplitText(unittest.TestCase):
    def test_basic_split(self):
        text = 'A b c. D e f. G h i.'
        s = scrape.split_text(text)
        self.assertEqual(s, [['A', 'b', 'c', '.'], ['D', 'e', 'f', '.'], ['G', 'h', 'i', '.']])

        text = 'A b c! D e f! G h i!'
        s = scrape.split_text(text)
        self.assertEqual(s, [['A', 'b', 'c', '!'], ['D', 'e', 'f', '!'], ['G', 'h', 'i', '!']])

        text = 'A b c? D e f? G h i?'
        s = scrape.split_text(text)
        self.assertEqual(s, [['A', 'b', 'c', '?'], ['D', 'e', 'f', '?'], ['G', 'h', 'i', '?']])

        text = 'A b c. D e f! G h i?'
        s = scrape.split_text(text)
        self.assertEqual(s, [['A', 'b', 'c', '.'], ['D', 'e', 'f', '!'], ['G', 'h', 'i', '?']])

    def test_split_with_parentheses(self):
        text = 'A b c. (D e) f. G h i.'
        s = scrape.split_text(text)
        self.assertEqual(s, [['A', 'b', 'c', '.'],
                             ['(', 'D', 'e', ')', 'f', '.'],
                             ['G', 'h', 'i', '.']])

        text = 'A b c. D (e f.) G h i.'
        s = scrape.split_text(text)
        self.assertEqual(s, [['A', 'b', 'c', '.'],
                             ['D', '(', 'e', 'f', '.', ')'],
                             ['G', 'h', 'i', '.']])

    def test_split_real_text(self):
        self.assertEqual(len(page), 296351)
        text = scrape.extract_text(page)

        spl = scrape.split_text(text)
        self.assertEqual(spl[13], ['It', 'is', 'necessary', 'because', 'indicative', 'sentences', 'of', 'ordinary', 'language', 'show', 'a', 'considerable', 'variety', 'of', 'form', 'and', 'complexity', 'that', 'makes', 'their', 'use', 'in', 'inference', 'impractical', '.'])
        self.assertEqual(spl[21], ['The', 'concrete', 'terms', '"man"', ',', '"mortal"', ',', 'etc', '.', ',', 'are', 'analogous', 'to', 'the', 'substitution', 'values', 'of', 'the', 'schematic', 'placeholders', 'P', ',', 'Q', ',', 'R', ',', 'which', 'were', 'called', 'the', '"matter"', '(', 'Greek', 'hyle', ')', 'of', 'the', 'inference', '.'])



def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(scrape))
    return tests


if __name__ == '__main__':
    unittest.main()
