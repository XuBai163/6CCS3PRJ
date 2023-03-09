import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer

nltk.download('punkt')

def tokenize_words(sentences):
    """
    Tokenize the given list of sentences into words and return a list of the words.
    
    Args:
        sentences (list of str): The sentences to be tokenized.
    
    Returns:
        list of str: The list of words.
    """
    return nltk.word_tokenize(sentences)

def stem(word):
    """
    Reduce a word to its stem using the Porter stemming algorithm.
    
    Args:
        word (str): The word to be stemmed.
    
    Returns:
        str: The stemmed word.
    """
    stemmer = nltk.PorterStemmer()
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, words):
    """
    Convert a tokenized sentence to a bag of words vector.
    
    Args:
        tokenized_sentence (list of str): The tokenized sentence to be converted to a bag of words vector.
        words (list of str): The list of all words in the dataset.
    
    Returns:
        bag (ndarry): The bag of words vector.
    """
    sentence_words = [stem(word) for word in tokenized_sentence]
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, word in enumerate(words):
        if word in sentence_words:
            bag[idx] = 1.0
    return bag