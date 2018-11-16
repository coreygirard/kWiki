import doctest
import unittest

from src.main import *


def get_page():
    with open("tests/tests.txt", "r") as f:
        page = f.read()
    return page


def test__get_page():
    page = get_page()
    assert len(page) == 296351


page = get_page()


def test__fetch_page():
    assert make_url("Web_scraping") == "http://en.wikipedia.org/wiki/Web_scraping"


def test__extract_title():
    page = get_page()
    assert extract_title(page) == "Logic"


def test__extract_links():
    page = get_page()
    links = extract_links(page)
    assert len(links) == 948
    assert links[10] == {
        "text": "Ethicists",
        "title": "List of ethicists",
        "url": "http://en.wikipedia.org/wiki/" "List_of_ethicists",
    }

    assert links[401] == {
        "text": "monotonicity of entailment",
        "title": "Monotonicity of entailment",
        "url": "http://en.wikipedia.org/wiki/" "Monotonicity_of_entailment",
    }


def test__extract_summary():
    page = get_page()
    summary = extract_summary(page)

    expected_prefix = "Logic (from the Ancient Greek: "
    assert summary.startswith(expected_prefix)

    expected_suffix = (
        "studied in computer science, linguistics, " + "psychology, and other fields."
    )
    assert summary.endswith(expected_suffix)


def test__extract_text():
    page = get_page()

    body = extract_text(page)
    assert body.startswith("Logic (from the Ancient Greek: ")
    assert body.endswith(
        "with a view to shocking conventional "
        'readers" in his book A History of Western Philosophy.'
    )


def test__split_into_sentences__basic():
    s = split_into_sentences
    assert s("A b c. D e f. G h i.") == ["A b c.", "D e f.", "G h i."]
    assert s("A b c! D e f! G h i!") == ["A b c!", "D e f!", "G h i!"]
    assert s("A b c? D e f? G h i?") == ["A b c?", "D e f?", "G h i?"]
    assert s("A b c. D e f? G h i!") == ["A b c.", "D e f?", "G h i!"]


def test__split_into_sentences__with_parentheses():
    s = split_into_sentences
    assert s("Abc def. Ghi jkl. Mno pqr.") == ["Abc def.", "Ghi jkl.", "Mno pqr."]
    assert s("Abc def. (Ghi) jkl. Mno pqr.") == ["Abc def.", "(Ghi) jkl.", "Mno pqr."]
    assert s("Abc def. Ghi (jkl). Mno pqr.") == ["Abc def.", "Ghi (jkl).", "Mno pqr."]
    assert s("Abc def. Ghi (jkl.) Mno pqr.") == ["Abc def.", "Ghi (jkl.)", "Mno pqr."]
    assert s("Abc def. Ghi (jkl) mno. Pqr.") == ["Abc def.", "Ghi (jkl) mno.", "Pqr."]


def test__split_words__basic():
    s = split_into_words
    assert s("A b c.") == ["A", "b", "c", "."]
    assert s("A b c!") == ["A", "b", "c", "!"]
    assert s("A b c?") == ["A", "b", "c", "?"]
    assert s("Abc def ghi.") == ["Abc", "def", "ghi", "."]
    assert s("Abc def ghi!") == ["Abc", "def", "ghi", "!"]
    assert s("Abc def ghi?") == ["Abc", "def", "ghi", "?"]


def test__split_words__with_parentheses():
    s = split_into_words
    assert s("(A b) c.") == ["(", "A", "b", ")", "c", "."]
    assert s("A (b) c.") == ["A", "(", "b", ")", "c", "."]
    assert s("A (b c).") == ["A", "(", "b", "c", ")", "."]
    assert s("A (b c.)") == ["A", "(", "b", "c", ".", ")"]


def test__split_text():
    assert split_text("A b c. D e f. G h i.") == [
        ["A", "b", "c", "."],
        ["D", "e", "f", "."],
        ["G", "h", "i", "."],
    ]

    assert split_text("A b c! D e f! G h i!") == [
        ["A", "b", "c", "!"],
        ["D", "e", "f", "!"],
        ["G", "h", "i", "!"],
    ]
    assert split_text("A b c? D e f? G h i?") == [
        ["A", "b", "c", "?"],
        ["D", "e", "f", "?"],
        ["G", "h", "i", "?"],
    ]
    assert split_text("A b c. D e f! G h i?") == [
        ["A", "b", "c", "."],
        ["D", "e", "f", "!"],
        ["G", "h", "i", "?"],
    ]


def test__split_text__with_parentheses():
    assert split_text("A b c. (D e) f. G h i.") == [
        ["A", "b", "c", "."],
        ["(", "D", "e", ")", "f", "."],
        ["G", "h", "i", "."],
    ]

    assert split_text("A b c. D (e f.) G h i.") == [
        ["A", "b", "c", "."],
        ["D", "(", "e", "f", ".", ")"],
        ["G", "h", "i", "."],
    ]


def test__split_text__real_text():
    page = get_page()
    text = extract_text(page)
    spl = split_text(text)
    assert spl[13] == [
        "It",
        "is",
        "necessary",
        "because",
        "indicative",
        "sentences",
        "of",
        "ordinary",
        "language",
        "show",
        "a",
        "considerable",
        "variety",
        "of",
        "form",
        "and",
        "complexity",
        "that",
        "makes",
        "their",
        "use",
        "in",
        "inference",
        "impractical",
        ".",
    ]

    assert spl[21] == [
        "The",
        "concrete",
        "terms",
        '"man"',
        ",",
        '"mortal"',
        ",",
        "etc",
        ".",
        ",",
        "are",
        "analogous",
        "to",
        "the",
        "substitution",
        "values",
        "of",
        "the",
        "schematic",
        "placeholders",
        "P",
        ",",
        "Q",
        ",",
        "R",
        ",",
        "which",
        "were",
        "called",
        "the",
        '"matter"',
        "(",
        "Greek",
        "hyle",
        ")",
        "of",
        "the",
        "inference",
        ".",
    ]
