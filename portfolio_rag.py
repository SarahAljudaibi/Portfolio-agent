import chromadb
import json
import os
import PyPDF2
from chromadb.config import Settings

class PortfolioRAG:
    def __init__(self, persist_directory="./chroma_db"):
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection_name = "sarah_portfolio"
        self.collection = self._get_or_create_collection()
    
    def _get_or_create_collection(self):
        """Get existing collection or create new one"""
        try:
            # Try to get existing collection
            collection = self.client.get_collection(name=self.collection_name)
            print(f"Found existing ChromaDB collection: {self.collection_name}")
            
            # Check if collection has data
            count = collection.count()
            if count == 0:
                print("Collection is empty, loading data...")
                self._load_all_data(collection)
            else:
                print(f"Collection has {count} documents")
            
            return collection
        except:
            # Create new collection if it doesn't exist
            print(f"Creating new ChromaDB collection: {self.collection_name}")
            collection = self.client.create_collection(name=self.collection_name)
            self._load_all_data(collection)
            return collection
    
    def _load_all_data(self, collection):
        """Load all portfolio data into ChromaDB"""
        print("Loading portfolio data...")
        
        self._load_github_data(collection)
        self._load_resume_data(collection)
        
        print("Portfolio data loaded successfully!")
    
    def _load_github_data(self, collection):
        """Load GitHub profile and repository data"""
        try:
            # Load GitHub profile
            profile_path = 'data/github data/github_profile.json'
            if os.path.exists(profile_path):
                with open(profile_path, 'r') as f:
                    profile = json.load(f)
                    collection.add(
                        documents=[f"Sarah's GitHub Profile: Name: {profile.get('name', 'N/A')}, Bio: {profile.get('bio', 'N/A')}, Location: {profile.get('location', 'N/A')}, Company: {profile.get('company', 'N/A')}, Public Repos: {profile.get('public_repos', 0)}, Followers: {profile.get('followers', 0)}"],
                        metadatas=[{"source": "github_profile", "type": "profile"}],
                        ids=["github_profile"]
                    )
                print("✓ GitHub profile loaded")
            
            # Load GitHub repositories
            repos_path = 'data/github data/github_repos.json'
            if os.path.exists(repos_path):
                with open(repos_path, 'r') as f:
                    repos = json.load(f)
                    for i, repo in enumerate(repos):
                        doc_text = f"Sarah's GitHub Repository: {repo['name']} - Description: {repo.get('description', 'No description')} - Language: {repo.get('language', 'N/A')} - Stars: {repo.get('stars', 0)} - URL: {repo.get('url', '')}"
                        collection.add(
                            documents=[doc_text],
                            metadatas=[{"source": "github_repos", "type": "repository", "repo_name": repo['name']}],
                            ids=[f"repo_{i}"]
                        )
                print(f"✓ {len(repos)} GitHub repositories loaded")
            
            # Load GitHub profile README
            readme_path = 'data/github data/github_profile_readme.md'
            if os.path.exists(readme_path):
                with open(readme_path, 'r', encoding='utf-8') as f:
                    readme = f.read()
                    collection.add(
                        documents=[f"Sarah's GitHub Profile README (Personal Background): {readme}"],
                        metadatas=[{"source": "github_readme", "type": "personal_background"}],
                        ids=["github_readme"]
                    )
                print("✓ GitHub profile README loaded")
                    
        except Exception as e:
            print(f"Error loading GitHub data: {e}")
    
    def _load_resume_data(self, collection):
        """Load resume PDF data"""
        try:
            data_dir = 'data'
            if not os.path.exists(data_dir):
                print("Data directory not found")
                return
                
            resume_files = [f for f in os.listdir(data_dir) if f.endswith('.pdf')]
            for i, resume_file in enumerate(resume_files):
                try:
                    with open(f'{data_dir}/{resume_file}', 'rb') as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        text = ""
                        for page in pdf_reader.pages:
                            text += page.extract_text()
                        
                        collection.add(
                            documents=[f"Sarah's Resume (Formal Background): {text}"],
                            metadatas=[{"source": "resume", "type": "formal_background", "filename": resume_file}],
                            ids=[f"resume_{i}"]
                        )
                    print(f"✓ Resume {resume_file} loaded")
                except Exception as e:
                    print(f"Error loading {resume_file}: {e}")
                    
        except Exception as e:
            print(f"Error loading resume data: {e}")
    
    def search(self, query, n_results=5):
        """Search portfolio data for relevant information"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results
        except Exception as e:
            print(f"Search error: {e}")
            return {"documents": [[]], "metadatas": [[]]}
    
    def get_summary(self):
        """Get a summary of Sarah's portfolio"""
        summary = """
Sarah is a data scientist and AI enthusiast with experience in:
• Machine Learning and AI projects
• Data analysis and visualization
• Python programming and Jupyter notebooks
• Real estate price forecasting using time series analysis
• Customer review analysis with sentiment detection
• Traffic accident analysis in Saudi Arabia

Her GitHub & Resmue showcases various data science projects including:
- Ryanair review analysis with AI-powered sentiment detection
- Time series forecasting for real estate valuation
- Traffic accidents analysis in KSA
- House prices prediction models
"""
        return summary.strip()
    
    def reload_data(self):
        """Reload all data (useful for updates)"""
        # Delete existing collection
        try:
            self.client.delete_collection(name=self.collection_name)
        except:
            pass
        
        # Create new collection and load data
        self.collection = self.client.create_collection(name=self.collection_name)
        self._load_all_data(self.collection)