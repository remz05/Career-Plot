
import pandas as pd
import gensim
import numpy as np
from gensim.models import Word2Vec, KeyedVectors

w2v_model=KeyedVectors.load_word2vec_format('/Users/ramyalather/Capstone_project_data/archive-2/' + "GoogleNews-vectors-negative300.bin", binary=True)

# creating a transformer class to take job tiles as input and convert them into word vectors

from sklearn.base import BaseEstimator, TransformerMixin

class word2vector(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        """the function takes a list of job titles and returns a feature matrix with columns as 300 word vectors and rows
   as job titles in the list X"""      
       
        job_title_list = [title.split() for title in X]
        feature_matrix = []
    
       
        
        for words in job_title_list: # Iterate through list of job titles
            row = []                 # Initialize an empty row in the feature matrix
            for word in words:       # Iterate through words in a job title 
                if word in w2v_model:
                    row.append(w2v_model[word])  # Append the word's vector representation to the row
            
                else:
                    row.append(np.zeros(300))
                    #bad_words.append(word)
                    
            feature_matrix.append(np.mean(row, axis=0).tolist())  # Append the avg of row vectors to the feature matrix
        return pd.DataFrame(feature_matrix)