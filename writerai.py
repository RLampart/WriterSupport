import re
#import tensorflow_hub as hub
#import matplotlib.pyplot as plt
#import pandas as pd
import re
#import seaborn as sns
#import tensorflow as tf
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
#USE_model = tf.compat.v2.saved_model.load('./universal_sentence_encoder')
# Path to save the model locally
local_model_path = './universal_sentence_encoder'

#def embed(input):
 # return USE_model(input)


vectorizer = TfidfVectorizer()


def pprocess(text):
    txt = []
    for t in text.split('\n'):
        bin = re.sub(r'[^a-zA-Z0-9\s]', '', t)
        if len(bin) > 0:
            txt.append(bin.lower())
    return txt


def cosine(u, v):
  v = np.transpose(v)
  return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

def cos(a,b):
  return (a * b.T).toarray()





def load(document):
   # Build the TF-IDF matrix
    document = pprocess(document)
    tfidf_matrixa = vectorizer.fit_transform(document)
    #tfidf_matrixb = embed(document)
    return document,tfidf_matrixa#, tfidf_matrixb
    

# Function to search for a term in the TF-IDF matrix
@app.route('/v1/references', methods=['POST'])
def search_term():
    # Transform the search term into the TF-IDF space
    print(request.headers)
    content = request.json
    document = content['doc']
    term = content['term']
    document,tfidf_matrixa = load(document)
    query_vectora = vectorizer.transform([term])
    #query_vectorb = embed([term])

    # Compute cosine similarities between the search term and all documents
    cosinea = cos(tfidf_matrixa, query_vectora)
    #cosineb = cosine(tfidf_matrixb, query_vectorb)
    cosine_similarities = cosinea#(cosinea + cosineb*70)/2

    # Get the indices of the documents sorted by similarity score (highest first)
    sorted_indices = np.argsort(cosine_similarities, axis=0)[::-1][:10]

    # Print the sorted document indices and their similarity scores
    print(f"Search results for '{term}':")
    results = []
    for idx in sorted_indices:
        results.append(f"Document {idx[0]}: {document[idx[0]]} (Score: {cosine_similarities[idx][0]})")
    return make_response(results,200)


# Example search term
# search_term("my way")

if __name__ == '__main__':
    app.run(debug = True, port=8080)


