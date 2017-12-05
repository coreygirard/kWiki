import unittest
import doctest
import scrape

def setUpModule():
    global page
    with open('tests.html','r') as f:
        page = f.read()

class TestFetch(unittest.TestCase):
    def test_fetch_page(self):
        page = scrape.fetchPage('Web_scraping')
        self.assertEqual(type(page),type('string'))
        self.assertTrue(len(page) > 10**3)

class TestExtract(unittest.TestCase):
    def test_extract_links(self):
        global page

        self.assertEqual(len(page),296351)

        links = scrape.extractLinks(page)

        self.assertEqual(len(links),948)

        self.assertEqual(links[10], {'url': 'List_of_ethicists', 'text': 'Ethicists', 'title': 'List of ethicists'})
        self.assertEqual(links[401], {'text': 'monotonicity of entailment', 'title': 'Monotonicity of entailment', 'url': 'Monotonicity_of_entailment'})

    def test_extract_summary(self):
        global page

        self.assertEqual(len(page),296351)

        summary = scrape.extractSummary(page)
        self.assertTrue(summary.startswith('Logic (from the Ancient Greek: '))
        self.assertTrue(summary.endswith('studied in computer science, linguistics, psychology, and other fields.'))

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(scrape))
    return tests


if __name__ == '__main__':
    unittest.main()
