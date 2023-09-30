import numpy as np
from src.nlp.embeddings import Embeddings
from src.nlp.autocomplete import Autocomplete
import src.data.db_connection as db


class Data:

    def __init__(self, docker=False) -> None:
        self.keywords, self.keywords_embeddings = Data.update_keywords_embeddings(docker=docker)
        # print(f"Total of {self.keywords_embeddings.shape[0]} filters")

        self.autocomplete = Autocomplete("src/data/searches.txt")
        # print(self.autocomplete.autocomplete_sentence("today I want Italian pizza for lunch", max_length=10))

    @staticmethod
    def update_keywords_embeddings(docker: bool) -> np.ndarray:
        cur = db.conn.cursor()
        cur.execute("SELECT name FROM filter_parameter")
        filters_list = [f[0] for f in list(cur.fetchall())]
        # print(filters_list)
        cur.close()
        model = Embeddings()
        return np.array(filters_list), np.array([model.get_sentence_embedding(f) for f in filters_list])
