import unittest
import doctest
import scrape

def setUpModule():
    global page
    with open('tests.txt','r') as f:
        page = f.read()

class TestFetch(unittest.TestCase):
    def test_fetch_page(self):
        page = scrape.fetchPage('Web_scraping')
        self.assertEqual(type(page),type('string'))
        self.assertTrue(len(page) > 10**3)

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

        self.assertEqual(links[10], {'url': 'List_of_ethicists', 'title': 'List of ethicists', 'text': 'Ethicists'})
        self.assertEqual(links[401], {'url': 'Monotonicity_of_entailment', 'title': 'Monotonicity of entailment', 'text': 'monotonicity of entailment'})

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

        body = scrape.extractBody(page)
        self.assertTrue(body.startswith('Logic (from the Ancient Greek: '))
        self.assertTrue(body.endswith('with a view to shocking conventional readers" in his book A History of Western Philosophy.'))

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(scrape))
    return tests


if __name__ == '__main__':
    unittest.main()
