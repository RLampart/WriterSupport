import os
import docx2txt
import fitz
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class Matrix():
    def __init__(self):
        self.matrix = None
        self.text = None
        self.origindoc = None
        self.vectorizer = TfidfVectorizer()
        files = self.get_files()
        if files == []:
            self.files = None
        else:
            self.files = files

    def get_files(self):
        files = []
        with open("files.txt","r") as f:
            file = f.readline()
            file = file[:-1]
            if file.endswith(".pdf") or file.endswith(".docx") or file.endswith(".txt"):
                files.append(file)
            f.close()
        return files 

    def read_doc_file(self,file):
        text = docx2txt.process(file)
        return text

    def read_txt_file(self,file):
      with open(file,'r') as f:   
        text = f.read()
        f.close()
      return text

    def read_pdf_file(self,file):
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
        pattern = r"(?<=\w|,|\s)\n(?=\w|,)"
        pdf_text = re.sub(pattern,' ', pdf_text)
        pdf_text = re.sub(r"\n●\n",'\n', pdf_text)
        return pdf_text

    def fullload(self):
        documents = {}
        if self.files == None:
            rootdir = os.getcwd()
            files = os.listdir(rootdir+'/files')
            docx_files = [file for file in files if file.endswith('.docx')]
            for doc in docx_files:
                doc_file = os.path.join('./files', doc)
                documents[doc] = self.read_doc_file(doc_file)
            pdf_files = [file for file in files if file.endswith('.pdf')]
            for pdf in pdf_files:
                pdf_file = os.path.join('./files', pdf)
                documents[pdf] = self.read_pdf_file(pdf_file)
            txt_files = [file for file in files if file.endswith('.txt')]
            for txt in txt_files:
                txt_file = os.path.join('./files', txt)
                documents[txt] = self.read_txt_file(txt_file)
            self.files = docx_files+pdf_files+txt_files
            self.text = documents
        elif self.text == None:
            docx_files = [file for file in self.files if file.endswith('.docx')]
            for doc in docx_files:
                doc_file = os.path.join('./files', doc)
                documents[doc] = self.read_doc_file(doc_file)
            pdf_files = [file for file in self.files if file.endswith('.pdf')]
            for pdf in pdf_files:
                pdf_file = os.path.join('./files', pdf)
                documents[pdf] = self.read_pdf_file(pdf_file)
            txt_files = [file for file in self.files if file.endswith('.txt')]
            for txt in txt_files:
                txt_file = os.path.join('./files', txt)
                documents[txt] = self.read_txt_file(txt_file)
            self.text = documents
        return self.text
    
    def pprocess(self,document):
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
    
    def load(self,document):
    # Build the TF-IDF matrix
        fdocument = self.fullload()
        if fdocument == {} and document == '':
            return []
        fdocument['Current Document'] = document 
        pdoc,odoc = self.pprocess(fdocument)
        self.matrix = self.vectorizer.fit_transform(pdoc)
        return odoc
    
    def get_range(self,docs):
        lens = []
        range = 0
        for key in docs:
            length = len(docs[key])
            range += length 
            lens.append((key,range))
        return lens
    
    def find_doc(self,lens,idx):
        count = 0
        for length in lens:
            if idx<length[1]:
                return length[0],count-1
            count += 1
    
    def cosine(self, u, v):
        v = np.transpose(v)
        return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

    def cos(self,b):
        return (self.matrix * b.T).toarray()