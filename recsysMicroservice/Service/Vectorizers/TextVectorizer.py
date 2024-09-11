import pickle
import torch
from transformers import BertTokenizer, BertModel
import numpy as np
import spacy
from spacy.tokens import Doc
from spacy.tokens import Token
from spacy.language import Language
from spacy.lang.en import stop_words


class TextVectorizer:

    def __init__(self) -> None:

        self.__nlp = self.__create_nlp()

        with open('../Models/TfidfVectorizer.pkl', 'rb') as file:
            self.__TfidfVectorizer = pickle.load(file)

        with open('../Models/CountVectorizer.pkl', 'rb') as file:
            self.__CountVectorizer = pickle.load(file)

        self.__bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.__bert_model = BertModel.from_pretrained('bert-base-uncased')

    @staticmethod
    def __create_nlp():

        Token.set_extension('is_stopword', default=False, force=True)
        Doc.set_extension('preprocessed_text', default='', force=True)

        nlp = spacy.load('en_core_web_sm')

        @Language.component("detect_stopwords")
        def detect_stopwords(doc: Doc):
            for token in doc:
                if (token.text.lower() in stop_words.STOP_WORDS) or (not token.is_alpha):
                    token._.is_stopword = True
            return doc

        @Language.component("add_preprocessed_text")
        def add_preprocessed_text(doc: Doc):
            preprocessed_tokens = []
            for token in doc:
                if not token._.is_stopword:
                    preprocessed_tokens.append(token.lemma_.lower())
                doc._.preprocessed_text = " ".join(preprocessed_tokens)
            return doc

        nlp.add_pipe('detect_stopwords', last=True)
        nlp.add_pipe('add_preprocessed_text', last=True)

        return nlp

    def __preprocess_text(self, text: str) -> str:
        doc = self.__nlp(text)
        return doc._.preprocessed_text

    def tfidf_vectorize(self, text: str) -> np.ndarray:
        preprocessed_text = self.__preprocess_text(text)
        vec = self.__TfidfVectorizer.transform([preprocessed_text])
        return vec.toarray()[0]

    def bert_vectorize(self, text: str) -> np.ndarray:

        preprocessed_text = self.__preprocess_text(text)

        tokens = self.__bert_tokenizer(preprocessed_text, padding=True, truncation=True, return_tensors="pt")

        with torch.no_grad():
            outputs = self.__bert_model(**tokens)

        return outputs.last_hidden_state.mean(dim=1).numpy()[0]

    def bow_vectorize(self, tokens: list) -> np.ndarray:
        preprocessed_tags = self.__preprocess_text(" ".join(tokens))
        return self.__CountVectorizer.transform([preprocessed_tags]).toarray()[0]
