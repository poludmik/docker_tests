import numpy as np
import psycopg2
from src.nlp.embeddings import Embeddings


class Data:

    def __init__(self, docker=False) -> None:
        self.keywords, self.keywords_embeddings = Data.update_keywords_embeddings(docker=docker)
        print(f"Total of {self.keywords_embeddings.shape[0]} filters")
    
    @staticmethod
    def update_keywords_embeddings(docker: bool) -> np.ndarray:
        print("Creating embeddings matrix from each filter/keyword...")

        db_connection_dict = {
            'dbname': 'develop',
            'user': 'testuser',
            'password': 'pleaseletmein',
        }

        if docker:
            db_connection_dict['host'] = 'db'
        else:
            db_connection_dict['host'] = 'localhost'
            db_connection_dict['port'] = 5432

        conn = psycopg2.connect(**db_connection_dict)
        cur = conn.cursor()
        cur.execute("SELECT name FROM filter_parameter")

        filters_list = [f[0] for f in list(cur.fetchall())]

        model = Embeddings()
        
        return np.array(filters_list), np.array([model.get_sentence_embedding(f) for f in filters_list])
        