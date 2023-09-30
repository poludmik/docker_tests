import numpy as np
import src.data.db_connection as db
import nltk
from nltk.corpus import words
nltk.download('words')

class Autocomplete:
    # ---------------- < Dictionary representation abandoned :( > -----------------
    # @staticmethod
    # def sample_word(dictionary):
    #     p0 = np.random.random()
    #     cumulative = 0
    #     for word, p in dictionary.items():
    #         cumulative += p
    #         if p0 < cumulative:
    #             return word
    #     assert(False)

    # @staticmethod
    # def generate1(first_order: dict[str, float]):
    #     sentence = []
    #     w0 = '<s>'
    #     while True:
    #         if len(sentence) > 8 or  w0 not in first_order:
    #             break
    #         w1 = Autocomplete.sample_word(first_order[w0])
    #         if w1 == '</s>':
    #             break
    #         sentence.append(w1)
    #         w0 = w1
    #     print(' '.join(sentence))

    # @staticmethod
    # def list_to_pdict(words): 
    #     d = {}
    #     n = len(words)
    #     for t in words: # count
    #         d[t] = d.get(t, 0.) + 1
    #     for t, c in d.items(): # normalize
    #         d[t] = c / n
    #     return d
    
    # @staticmethod
    # def add2dict_1st(dictionary, key, value):
    #     if key not in dictionary:
    #         dictionary[key] = []
    #     dictionary[key].append(value)

    # @staticmethod
    # def get_n_gram_probabilities(txt_file_name: str):
        # # dict or matrix with word2

        # translation_table = str.maketrans('', '', '.,')
        # first_order = {} # the 1st order transition "tensor" of probabilities
        # for line in open(txt_file_name):

        #     tokens = line.translate(translation_table).rstrip().split()
        #     if not tokens:
        #         continue

        #     tokens = ['<s>'] + tokens + ['</s>']

        #     for i in range(len(tokens)-1):
        #         # measure all the words distribution given one previous word
        #         Autocomplete.add2dict_1st(first_order, tokens[i], tokens[i+1])

        # # for key, value in first_order.items():
        # #     print(key,':',value)

        # for word, nexts in first_order.items():
        #     first_order[word] = Autocomplete.list_to_pdict(nexts)

        # # for key, value in first_order.items():
        # #     print(key,':',value)

        # for _ in range(5):
        #     Autocomplete.generate1(first_order=first_order)


    # ---------------- Matrix representation -----------------

    def __init__(self, corpus_file_name: str):
        input_file_name = corpus_file_name
        changed_file_name = corpus_file_name.replace('.txt', '_modified') + ".txt"
        self.translation_table = str.maketrans('', '', '.,')
        with open(input_file_name, "r") as input_file, open(changed_file_name, "w") as output_file:
            for line in input_file:
                tokens = line.translate(self.translation_table).rstrip().split()
                output_file.write(' '.join(tokens) + '\n')
        self.text = changed_file_name
        self.word2idx, self.idx2word = self.__get_word2idx(self.text)
        self.count_matrix = self.__get_count_bigram_matrix(self.text, self.word2idx, smoothing=False)
        self.bigram_matrix = self.__count_matrix_to_bigram_matrix(self.count_matrix)

    def sample_next_word(self, prev_word: str):
        # return self.idx2word[np.argmax(self.bigram_matrix[self.word2idx[prev_word]])]
        prev_word = self.__check_prev_word(prev_word)
        return self.idx2word[np.random.choice(len(self.word2idx), 1, p=self.bigram_matrix[self.word2idx[prev_word]])[0]]
    
    def sample_top_n_words(self, prev_word: str, N: int): # non zero values only (e.g. exclude "<UNK>")
        prev_word = self.__check_prev_word(prev_word)
        arr = self.bigram_matrix[self.word2idx[prev_word]][:-1]
        ind = arr.argsort()
        return [self.idx2word[i] for i in ind[arr[ind] != 0.0]][::-1][:N]
    
    def sample_n_next_words(self, prev_word: str, N: int):
        prev_word = self.__check_prev_word(prev_word)
        return [self.idx2word[w] for w in np.random.choice(len(self.word2idx), N, p=self.bigram_matrix[self.word2idx[prev_word]]).tolist()]

    def autocomplete_list_of_tokens(self, tokens: list[str], max_len: int = 7) -> str:
        print(tokens)
        if len(tokens) > 0:
            w0 = tokens[-1]
        else:
            w0 = "<s>"
        while w0 != '</s>':
            if len(tokens) >= max_len:
                break
            w1 = self.sample_next_word(w0)
            if w1 == '</s>':
                break
            tokens.append(w1)
            w0 = w1
        return ' '.join(tokens)

    def autocomplete_sentence(self, sentence: str, max_length: int = 7, N_proposed_words: int = 5) -> tuple[str, list[str]]:
        tokens = sentence.translate(self.translation_table).rstrip().split()
        last_word = tokens[-1]
        ridiculous_sent_completion = ''

        # User has inserted char that is not a letter (previous word finished)
        if not sentence[-1].isalpha():
            next_words = self.sample_n_next_words(prev_word=last_word, N=N_proposed_words)
            ridiculous_sent_completion = self.autocomplete_list_of_tokens(tokens + [next_words[0]], max_len=max_length)
        else: # Last char is a letter
            cur = db.conn.cursor()
            cur.execute(f"SELECT name from filter_parameter WHERE search_tsv @@ to_tsquery('simple', '{last_word}:*');")
            possible_words_after_completion = list(w[0] for w in cur.fetchall())
            cur.close()

            print(possible_words_after_completion)

            if len(possible_words_after_completion) > 0:
                if last_word in possible_words_after_completion or last_word.lower() in possible_words_after_completion: # finished word, insert ' ' and complete
                    next_words = self.sample_n_next_words(prev_word=last_word, N=N_proposed_words)
                    ridiculous_sent_completion = self.autocomplete_list_of_tokens(tokens + [next_words[0]], max_len=max_length)
            else:
                pass
                
        print("rid_completion:", ridiculous_sent_completion)
        print("next_words:", next_words)
        

        # if last_word in db or last_word in words.words():
        #     # last word is complete
        #     return sentence + " " + sample_sentence(w0=last_word, max_len=max_length-len(tokens))
        # else:
        #     # complete the word if possible and complete sentence with this word

    def __check_prev_word(self, prev_word: str):
        if prev_word not in self.word2idx:
            if prev_word.lower() in self.word2idx:
                prev_word = prev_word.lower()
            else:
                prev_word = "<UNK>"
        return prev_word

    @staticmethod
    def __get_word2idx(text: str) -> dict[str, int]:
        word2idx = {}
        idx2word = {}
        f = text
        if type(text) != list:
            f = open(text)
        for line in f:
            tokens = line.rstrip().split()
            if not tokens:
                continue
            tokens = ['<s>'] + tokens + ['</s>']
            for i in range(len(tokens)):
                if tokens[i] not in word2idx:
                  word2idx[tokens[i]] = len(word2idx)
                  idx2word[len(idx2word)] = tokens[i]
        word2idx["<UNK>"] = len(word2idx)
        idx2word[len(idx2word)] = "<UNK>"
        return word2idx, idx2word
    
    @staticmethod
    def __get_count_bigram_matrix(text, word2idx: dict[str, int], smoothing: bool = False) -> np.ndarray:
        count_matrix = np.zeros((len(word2idx), len(word2idx)))

        f = text
        if type(text) != list:
            f = open(text)

        for line in f:
            tokens = line.rstrip().split()
            if not tokens:
                continue
            tokens = ['<s>'] + tokens + ['</s>']
            for i in range(len(tokens) - 1):
                token = tokens[i]
                token_next = tokens[i + 1]
                if token not in word2idx:
                    token = "<UNK>"
                if token_next not in word2idx:
                    token_next = "<UNK>"
                count_matrix[word2idx[token], word2idx[token_next]] += 1
        if smoothing:
            count_matrix = count_matrix + 1
        
        # will sample randomly if word wasn't seen before
        count_matrix[word2idx["<UNK>"]] = 1 # np.sum(count_matrix, axis=0) / np.sum(count_matrix)
        return count_matrix
    
    @staticmethod
    def __count_matrix_to_bigram_matrix(count_matrix: np.ndarray) -> np.ndarray:
        row_sums = count_matrix.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0.0] = 1.0 # to avoid division by zero
        new_matrix = count_matrix / row_sums
        return new_matrix


if __name__ == "__main__":
    autocomplete = Autocomplete("src/data/searches.txt")
    # for _ in range(5):
    #     print(autocomplete.sample_sentence(7))

    # print(autocomplete.sample_top_n_words("I", 5))

