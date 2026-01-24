import os
import json
from pypdf import PdfReader
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

class PortfolioRAG:
    def __init__(self, data_folder="data"):
        self.data_folder = data_folder
        self.client = chromadb.Client(Settings(anonymized_telemetry=False, allow_reset=True))
        self.collection = self.client.get_or_create_collection(name="portfolio")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.initialize_rag()
    
    def initialize_rag(self):
        if self.collection.count() > 0:
            return
        
        documents = []
        metadatas = []
        ids = []
        
        # Process PDFs
        for root, _, files in os.walk(self.data_folder):
            for file in files:
                filepath = os.path.join(root, file)
                
                if file.endswith('.pdf'):
                    text = self._extract_pdf(filepath)
                    documents.append(text)
                    metadatas.append({"source": file, "type": "pdf"})
                    ids.append(f"pdf_{len(ids)}")
                
                elif file.endswith('.json'):
                    data = self._extract_json(filepath)
                    documents.append(data)
                    metadatas.append({"source": file, "type": "json"})
                    ids.append(f"json_{len(ids)}")
                
                elif file.endswith('.md'):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        text = f.read()
                    documents.append(text)
                    metadatas.append({"source": file, "type": "markdown"})
                    ids.append(f"md_{len(ids)}")
        
        if documents:
            self.collection.add(documents=documents, metadatas=metadatas, ids=ids)
    
    def _extract_pdf(self, filepath):
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    
    def _extract_json(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return json.dumps(data, indent=2)
    
    def retrieve(self, query, n_results=3):
        results = self.collection.query(query_texts=[query], n_results=n_results)
        return results['documents'][0] if results['documents'] else []
