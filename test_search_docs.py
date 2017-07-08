"""testing for module seach_docs.py
"""
import glob
import search_docs as sd

def test_get_file_map_len():
    """test for get_file_map length
    """
    file_map = sd.get_file_map("resources/")
    files = glob.glob("resources/" + "/**" + ".txt", recursive=True)
    assert len(file_map) == len(files)


def test_get_file_map_type():
    """test for get_file_map filetypes
    """
    for file in sd.get_file_map("resources/"):
        assert file.endswith(".txt")

def test_get_texts_ignores():
    """test for texts ignorechars
    """
    file_map = sd.get_file_map(".")
    texts = sd.get_texts(file_map)
    ingnores = "[:.,;:!?\"-()]\n".split()
    for text in texts:
        for char in ingnores:
            assert text.find(char) == -1


def test_get_texts_size():
    """test for texts size
    """
    file_map = sd.get_file_map("resources/")
    texts = [i for i in sd.get_texts(file_map)]
    assert len(file_map) == len(texts)
    for file, text in zip(file_map, texts):
        with open(file, "r", "utf-8") as myfile:
            test_text = myfile.read()
        assert len(test_text) == len(text)

def test_get_stopwords():
    """test get_stopwords if there are any loaded
    """
    stopwords = sd.get_stopwords("resources/stopwords.de.json")
    assert len(stopwords) > 0
