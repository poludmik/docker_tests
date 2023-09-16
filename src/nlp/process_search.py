from dataclasses import dataclass
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.metrics import distance
from nltk import ngrams
import numpy as np
import re
from typing import List
from src.data.data import Data
from src.nlp.embeddings import Embeddings


nltk.download('stopwords') # set of stop words
nltk.download('wordnet') # lemmatizer
nltk.download('averaged_perceptron_tagger') # part-of-speech tagger

@dataclass
class Pair:
    query_w: str
    matched_w: str

    def __repr__(self):
        return f"{self.query_w}-{self.matched_w}"

class ProcessSearch():

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    model = Embeddings()

    # https://www.guru99.com/pos-tagging-chunking-nltk.html
    pos_excluded = ["MD", "VB", "VBP", "VBN", "VBZ", "VBG", "VBD", "RB", "CC", "WRB"] 
    
    negations = ["no", "without", "except"] 

    @staticmethod
    def get_keywords(sentence: str, data: Data) -> List[str]:

        # Remove punctuation and trailing chars, lowercase and split
        tokens_list = re.sub(r'[^\w\s]','', sentence).rstrip().lower().split()

        exclude = []
        for i in range(len(tokens_list) - 1):
            if tokens_list[i] in ProcessSearch.negations:
                exclude.append(ProcessSearch.lemmatizer.lemmatize(tokens_list[i+1]))

        # Remove verbs and useless part-of-speeches
        pos = nltk.pos_tag(tokens_list)
        words = [t[0] for t in pos if t[1] not in ProcessSearch.pos_excluded]

        # Sets are faster, but order is not preserved (for testing purposes using a list)
        # words = set(words) - ProcessSearch.stop_words
        words = [w for w in words if w not in ProcessSearch.stop_words]

        words = [ProcessSearch.lemmatizer.lemmatize(w) for w in words]

        # also take 2-grams
        ngram_list = []
        for ng in ngrams(words, 2):
            ngram_list.append(' '.join(ng))
        words += ngram_list

        w_embs = np.array([ProcessSearch.model.get_sentence_embedding(t) for t in words])
        print(w_embs.shape)
        print(data.keywords_embeddings.T.shape)
        sim_threshold = 0.88
        multiplied = w_embs @ data.keywords_embeddings.T
        print(multiplied.shape)

        # # Only for logs and tests
        # idxs_request_similarity = np.max(multiplied, axis=1) >= sim_threshold
        # res_req = np.array(words)[idxs_request_similarity].tolist()
        # print(f"Similar from request list: {res_req}")

        idxs_keyword_similarity = np.max(multiplied, axis=0) >= sim_threshold
        res = data.keywords[idxs_keyword_similarity].tolist()
        print(f"Similar from filters list: {res}")

        res_pairs = []
        for w in words:
            for kw in data.keywords:
                if kw not in res and ProcessSearch.__compare_levenshtein(w, kw):
                    res.append(kw)
                    res_pairs.append(Pair(w, kw))
        print(res_pairs, end="\n\n")

        return res, [t for t in exclude if t in res]

    @staticmethod
    def __compare_levenshtein(w1: str, w2: str, max_difference: int = 1) -> bool:
        return distance.edit_distance(w1, w2) <= max_difference
    
    @staticmethod
    def __compare_with_embs(w1: str, w2: str, sim_threshold: int = 0.8) -> bool:
        emb1 = ProcessSearch.model.get_sentence_embedding(w1)
        emb2 = ProcessSearch.model.get_sentence_embedding(w2)
        return (emb1 @ emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)) >= sim_threshold


if __name__ == "__main__":
    user_request = "I want Japnse foods for a cheap price, maybe sushi with fish or pasta"
    keywords = ["sushi", "pizza", "burger", "japanese", "italian", "seafood", 
                                             "cheap", "fastfood", "meat", "steak", "fish", "chips", "spaghetti",
                                             "american", "wine", "coctail", "russian", "tortilla", "coffee", "capuccino",
                                             "breakfast", "dinner", "chinese", "schnitzel", "pirogi", "czech"]
    res = ProcessSearch.get_keywords(sentence=user_request, keyword_list=keywords)
    print('\x1b[1;34m' + "Asked for: " + '\x1b[0m' + f"'{user_request}'")
    print('\x1b[1;34m' + "Extracted keywords: " + '\x1b[0m' + f"{res}")
    
