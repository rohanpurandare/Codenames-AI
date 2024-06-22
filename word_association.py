from wiki import create_word_dict
from tfIdf import computeTF, computeIDF, computeTFIDF
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import nltk
nltk.download('stopwords')

class WordAssociation:
    def __init__(self):
        self.word_page_dict = []
        self.word_bank = []
        self.tf_idf_vectors = []
        self.cosine_similarity_matrix = []
        with open("wordbank.txt") as file:
            self.word_bank = file.read().splitlines()

    #create tf-idf vectors for all possible words on the board
    def create_tf_idf_vectors(self, word_bank):

        try:
            with open('tf.vector', 'rb') as file:
                self.tf_idf_vectors = pickle.load(file)
                # self.prune_tf_idf_vectors(0.0001)
                return self.tf_idf_vectors
        except:
            pass

        if len(self.word_page_dict) == 0:
            self.word_page_dict = create_word_dict(word_bank)
        word_page_dict = self.word_page_dict

        stop_words = set(stopwords.words('english'))

        total = set()
        frequencyDict = {}
        tfDict = {}
        tfIdfDict = {}

        #filter the doc (wikipidia article for each word) and union corpus to find all vocab words
        for word in word_page_dict:
            word_corpus = word_page_dict[word].split(' ')
            filtered_corpus = [w for w in word_corpus if (not w in stop_words and not w.lower() == word)]
            word_page_dict[word] = filtered_corpus
            total= set(total).union(set(filtered_corpus))

        for word in word_page_dict:
            frequencyDict[word] = dict.fromkeys(total, 0)
            tfDict[word] = dict.fromkeys(total, 0)

        #calculate frequency of words in each article
        for word in frequencyDict:
            for each_word in word_page_dict[word]:
                frequencyDict[word][each_word]+=1
        #compute term frequenct based on frequenct observed
        for word in frequencyDict:
            tfDict[word] = computeTF(frequencyDict[word], word_page_dict[word])

        #compute idf
        idfs = computeIDF([frequencyDict[word] for word in frequencyDict])

        for word in frequencyDict:
            tfIdfDict[word] = computeTFIDF(tfDict[word], idfs)

        with open('tf.vector', 'wb') as file:
            pickle.dump(tfIdfDict, file, -1)

        self.tf_idf_vectors = tfIdfDict
        # self.prune_tf_idf_vectors(0.0001)
        return tfIdfDict

    def prune_tf_idf_vectors(self, threshold):
        for board_word in self.tf_idf_vectors:
            for word in list(self.tf_idf_vectors[board_word].keys()):
                if self.tf_idf_vectors[board_word][word] <= threshold:
                    del self.tf_idf_vectors[board_word][word]

    #create the cosine word matrix for board words. (matrix of size n x n where n is all possible board words)
    def create_cosine_word_matrix(self, tf_idf_dictonary):
        param = []
        for board_word in tf_idf_dictonary.keys():
            tfIdfVals = [tf_idf_dictonary[board_word][x] for x in tf_idf_dictonary[board_word].keys()]
            param.append(tfIdfVals)

        cosine_matrix = cosine_similarity(param)
        self.cosine_similarity_matrix = cosine_matrix
        return cosine_matrix

    #returns all vocab words that match to a given board word based on their tf-idf ratings
    def ratings(self, board_word, tf_idf_rating):
        if len(self.tf_idf_vectors) == 0:
            self.create_tf_idf_vectors(self.word_bank)
        tf_df_dict = self.tf_idf_vectors
        vocab_words = []
        for vocab_word in tf_df_dict[board_word]:
            if tf_df_dict[board_word][vocab_word] >= tf_idf_rating:
                vocab_words.append(vocab_word)

        return vocab_words

    def similarity(self, board_word, clue_word):
        if len(self.tf_idf_vectors) == 0:
            self.create_tf_idf_vectors(self.word_bank)
        tf_df_dict = self.tf_idf_vectors
        if clue_word in tf_df_dict[board_word]:
            return tf_df_dict[board_word][clue_word]
        else:
            return 0

    # returns other board words similar to a given board word with cosine similarity higher than benchmark
    def get_similar_board_words(self, board_word, benchmark):
        if len(self.cosine_similarity_matrix) == 0:
            self.create_cosine_word_matrix(self.tf_idf_vectors)
        cosine_matrix = self.cosine_similarity_matrix
        similar_words_index = []
        word_index = self.word_bank.index(board_word)
        for i in  range(len(cosine_matrix[word_index])):
            if cosine_matrix[word_index][i] >= benchmark:
                similar_words_index.append(i)

        similar_words = [self.word_bank[i] for i in similar_words_index]
        return similar_words
