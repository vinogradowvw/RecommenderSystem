import unittest
from recsysMicroservice.Service.Vectorizers.TextVectorizer import TextVectorizer
import yaml

with open("./recsysMicroservice/config.yml", "r") as file:
    config = yaml.safe_load(file)

class TextVectorizerUnitTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._vectorizer = TextVectorizer()

    def test_tfidf_vectorize():
        pass

    def test_bow_vectorize():
        pass

    def test_bert_vectorize():
        pass
