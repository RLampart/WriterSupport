import os
import re
import numpy as np
from flask import Flask, request, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename
from matrix import Matrix


app = Flask(__name__)
CORS(app) 
tfidmatrix = Matrix()


@app.route('/v1/upload', methods=['POST'])
def upload():
    content = request.files['files']
    filename = secure_filename(content.filename)
    content.save(os.path.join('./files', filename))
    tfidmatrix.matrix = None
    tfidmatrix.load('')
    return make_response({"msg":filename+" Received"},201)

@app.route('/v1/removeDoc', methods=['POST'])
def remove():
    content = request.json['file']
    path = os.path.join('./files', content)
    if os.path.exists(path):
       os.remove(path)
       msg = content+" has been deleted"
       tfidmatrix.matrix = None
       tfidmatrix.load('')
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
    docs = tfidmatrix.load(document)
    lens = tfidmatrix.get_range(docs)
    query_vector = tfidmatrix.vectorizer.transform([term])

    # Compute cosine similarities between the search term and all documents
    cosine_similarities = tfidmatrix.cos(query_vector)

    # Get the indices of the documents sorted by similarity score (highest first)
    sorted_indices = np.argsort(cosine_similarities, axis=0)[::-1]

    # Print the sorted document indices and their similarity scores
    results = []
    for idx in sorted_indices:
        if cosine_similarities[idx][0] > 0.1:
           doc,prev = tfidmatrix.find_doc(lens,idx[0])
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


