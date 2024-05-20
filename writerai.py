import docx2txt
import re
from sklearn.model_selection import train_test_split
import tensorflow as tf
from transformers import pipeline, TFAutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import fitz
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import os
import pandas as pd
import re
import seaborn as sns

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
USE_model = hub.load(module_url)
print ("module %s loaded" % module_url)
def embed(input):
  return USE_model(input)

def read_doc_file(file_path):
  text = docx2txt.process(file_path)
  return text

# Example usage
file_path = 'Legends.docx'
doc_text = read_doc_file(file_path)

document = fitz.open("EZ Apocalypse.pdf")
pdf_text = ""

# Iterate through each page
for page_num in range(len(document)):
    # Select the page
    page = document.load_page(page_num)

    # Extract text from the page while preserving white spaces
    pdf_text += page.get_text("text")

# Close the document
document.close()



# Combine the text from both files
combined_text = doc_text + pdf_text

# Process the combined text as needed

def pprocess(text):
    txt = []
    for t in text.split('\n'):
        bin = re.sub(r'[^a-zA-Z0-9\s]', '', t)
        if len(bin) > 0:
            txt.append(bin.lower())
    return txt


clean_doc = pprocess(doc_text)
clean_pdf = pprocess(pdf_text)
clean_combined = pprocess(combined_text)

def cosine(u, v):
  v = np.transpose(v)
  return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

def cos(a,b):
  return (a * b.T).toarray()

# Sample document corpus
documents = clean_combined

# Initialize the TfidfVectorizer
vectorizer = TfidfVectorizer()

# Build the TF-IDF matrix
tfidf_matrixa = vectorizer.fit_transform(documents)
tfidf_matrixb = embed(documents)

# Function to search for a term in the TF-IDF matrix
def search_term(term):
    # Transform the search term into the TF-IDF space
    query_vectora = vectorizer.transform([term])
    query_vectorb = embed([term])

    # Compute cosine similarities between the search term and all documents
    cosinea = cos(tfidf_matrixa, query_vectora)
    cosineb = cosine(tfidf_matrixb, query_vectorb)
    cosine_similarities = (cosinea + cosineb*70)/2

    # Get the indices of the documents sorted by similarity score (highest first)
    sorted_indices = np.argsort(cosine_similarities, axis=0)[::-1][:10]

    # Print the sorted document indices and their similarity scores
    print(f"Search results for '{term}':")
    for idx in sorted_indices:
        print(f"Document {idx[0]}: {documents[idx[0]]} (Score: {cosine_similarities[idx][0]})")

# Example search term
search_term("my way")