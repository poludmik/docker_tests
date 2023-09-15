from dataclasses import dataclass
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.metrics import distance
from sentence_transformers import SentenceTransformer
import numpy as np
import torch
import re
from typing import List


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
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(device)
    gte_model = SentenceTransformer('thenlper/gte-base', device=device)

    # https://www.guru99.com/pos-tagging-chunking-nltk.html
    pos_excluded = ["MD", "VB", "VBP", "VBN", "VBZ", "VBG", "VBD", "RB", "CC", "WRB"] 
    
    @staticmethod
    def get_keywords(sentence: str, keyword_list: List[str]) -> List[str]:

        # Remove punctuation and trailing chars, lowercase and split
        tokens_list = re.sub(r'[^\w\s]','', sentence).rstrip().lower().split()

        # Remove verbs and useless part-of-speeches
        pos = nltk.pos_tag(tokens_list)
        words = [t[0] for t in pos if t[1] not in ProcessSearch.pos_excluded]

        # Sets are faster, but order is not preserved (for testing purposes using a list)
        # words = set(words) - ProcessSearch.stop_words
        words = [w for w in words if w not in ProcessSearch.stop_words]

        words = [ProcessSearch.lemmatizer.lemmatize(w) for w in words]
        
        res_pairs = []
        for w in words:
            for kw in keyword_list:
                # Either differ in at most max_difference chars or embeddings cosine similarity is close to 1 (pasta-spaghetti)
                if ProcessSearch.__compare_levenshtein(w, kw) or ProcessSearch.__compare_with_gte(w, kw, 0.9):
                    res_pairs.append(Pair(w, kw))
        print(res_pairs, end="\n\n")

        return [p.matched_w for p in res_pairs]

    @staticmethod
    def __compare_levenshtein(w1: str, w2: str, max_difference: int = 2) -> bool:
        return distance.edit_distance(w1, w2) <= max_difference
    
    @staticmethod
    def __compare_with_gte(w1: str, w2: str, sim_threshold: int = 0.85) -> bool:
        emb1 = ProcessSearch.gte_model.encode(w1)
        emb2 = ProcessSearch.gte_model.encode(w2)
        return (emb1 @ emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)) > sim_threshold


if __name__ == "__main__":
    user_request = "I want Japnse foods for a cheap price, maybe sushi with fish or pasta"
    keywords = ["sushi", "pizza", "burger", "japanese", "italian", "seafood", 
                                             "cheap", "fastfood", "meat", "steak", "fish", "chips", "spaghetti",
                                             "american", "wine", "coctail", "russian", "tortilla", "coffee", "capuccino",
                                             "breakfast", "dinner", "chinese", "schnitzel", "pirogi", "czech"]
    res = ProcessSearch.get_keywords(sentence=user_request, keyword_list=keywords)
    print('\x1b[1;34m' + "Asked for: " + '\x1b[0m' + f"'{user_request}'")
    print('\x1b[1;34m' + "Extracted keywords: " + '\x1b[0m' + f"{res}")
    
