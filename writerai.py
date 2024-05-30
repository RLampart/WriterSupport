import os
import docx2txt
import fitz
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, request, make_response
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

def read_txt_file(file):
  with open(file,'r') as f:   
      text = f.read()
      f.close()
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

def pprocess(document):
    ptxt = []
    odoc = {}
    for key in document:
        text = document[key]
        otxt = []
        for t in text.split('\n'):
            bin = re.sub(r'[^a-zA-Z0-9\s]', '', t)
            if len(bin) > 0:
                ptxt.append(bin.lower())
                otxt.append(t)
        odoc[key] = otxt
    return ptxt,odoc


def cosine(u, v):
  v = np.transpose(v)
  return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

def cos(a,b):
  return (a * b.T).toarray()

def fullload():
    rootdir = os.getcwd()
    documents = {}
    files = os.listdir(rootdir+'/files')
    docx_files = [file for file in files if file.endswith('.docx')]
    for doc in docx_files:
        doc_file = os.path.join('./files', doc)
        documents[doc] = read_doc_file(doc_file)
    pdf_files = [file for file in files if file.endswith('.pdf')]
    for pdf in pdf_files:
        pdf_file = os.path.join('./files', pdf)
        documents[pdf] = read_pdf_file(pdf_file)
    txt_files = [file for file in files if file.endswith('.txt')]
    for txt in txt_files:
        txt_file = os.path.join('./files', txt)
        documents[txt] = read_txt_file(txt_file)
    return documents


def load(document):
   # Build the TF-IDF matrix
    fdocument = fullload()
    fdocument['Current Document'] = document 
    pdoc,odoc = pprocess(fdocument)
    tfidf_matrixa = vectorizer.fit_transform(pdoc)
    #tfidf_matrixb = embed(document)
    return odoc,tfidf_matrixa#, tfidf_matrixb

def get_range(docs):
    lens = []
    range = 0
    for key in docs:
        length = len(docs[key])
        range += length 
        lens.append((key,range))
    return lens

def find_doc(lens,idx):
    count = 0
    for length in lens:
        if idx<length[1]:
            return length[0],count-1
        count += 1

@app.route('/v1/upload', methods=['POST'])
def upload():
    content = request.files['files']
    filename = secure_filename(content.filename)
    content.save(os.path.join('./files', filename))
    return make_response({"msg":"File Received"},201)

@app.route('/v1/removeDoc', methods=['POST'])
def remove():
    content = request.json['file']
    path = os.path.join('./files', content)
    if os.path.exists(path):
       os.remove(path)
       msg = content+" has been deleted"
    else:
       msg = content+" does not exist"
    return make_response({"msg":msg},200)

@app.route('/v1/files', methods=['GET'])
def get_files():
    rootdir = os.getcwd()
    files = os.listdir(rootdir+'/files')
    docx_files = [file for file in files if file.endswith('.docx')]
    pdf_files = [file for file in files if file.endswith('.pdf')]
    txt_files = [file for file in files if file.endswith('.txt')]
    filelist = docx_files+pdf_files+txt_files
    return make_response(filelist,200)
    

# Function to search for a term in the TF-IDF matrix
@app.route('/v1/references', methods=['POST'])
def search_term():
    # Transform the search term into the TF-IDF space
    content = request.json
    document = content['doc']
    term = content['term']
    docs,tfidf_matrixa = load(document)
    lens = get_range(docs)
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
        if cosine_similarities[idx][0] > 0.1:
           doc,prev = find_doc(lens,idx[0])
           if prev<0:
               num = idx[0]
           else:
               num = idx[0]-lens[prev][1]
           results.append(f"{doc} Line {num+1}: {docs[doc][num]} (Score: {cosine_similarities[idx][0]})")
        else:
           break
    results.append(len(document))
    return make_response(results,200)

if __name__ == '__main__':
    app.run(debug = True, port=8080)


