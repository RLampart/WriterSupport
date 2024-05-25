import os
import docx2txt
import fitz
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
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app) 
#USE_model = tf.compat.v2.saved_model.load('./universal_sentence_encoder')
# Path to save the model locally
local_model_path = './universal_sentence_encoder'

#def embed(input):
 # return USE_model(input)


vectorizer = TfidfVectorizer()

def read_doc_file(file):
  text = docx2txt.process(file)
  return text

def read_pdf_file(file):
    document = fitz.open(file)
    pdf_text = ""
    # Iterate through each page
    for page_num in range(len(document)):
        # Select the page
        page = document.load_page(page_num)
        # Extract text from the page while preserving white spaces
        pdf_text += page.get_text("text")
    # Close the document
    document.close()
    return pdf_text

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

def fullload():
    rootdir = os.getcwd()
    files = os.listdir(rootdir+'/files')
    docx_files = [file for file in files if file.endswith('.docx')]
    doc_text = ''
    for doc in docx_files:
        doc_text += read_doc_file(doc)
        doc_text += '\n'
    pdf_files = [file for file in files if file.endswith('.pdf')]
    pdf_text = ''
    for pdf in pdf_files:
        pdf += read_pdf_file(pdf)
        pdf += '\n'
    return doc_text+pdf_text


def load(document):
   # Build the TF-IDF matrix
    fdocument = fullload()
    document = fdocument+'\n'+document
    rdoc = pprocess(document)
    tfidf_matrixa = vectorizer.fit_transform(rdoc)
    #tfidf_matrixb = embed(document)
    return rdoc,tfidf_matrixa#, tfidf_matrixb

@app.route('/upload', methods=['POST'])
def upload():
    content = request.files['files']
    filename = secure_filename(content.filename)
    content.save(os.path.join('./files', filename))
    return make_response("Received",200)
    

# Function to search for a term in the TF-IDF matrix
@app.route('/v1/references', methods=['POST'])
def search_term():
    # Transform the search term into the TF-IDF space
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
    sorted_indices = np.argsort(cosine_similarities, axis=0)[::-1]

    # Print the sorted document indices and their similarity scores
    results = []
    for idx in sorted_indices:
        if cosine_similarities[idx][0] > 0:
           results.append(f"Paragraph {idx[0]+1}: {document[idx[0]]} (Score: {cosine_similarities[idx][0]})")
        else:
           break
    results.append(len(document))
    return make_response(results,200)

if __name__ == '__main__':
    app.run(debug = True, port=8080)


