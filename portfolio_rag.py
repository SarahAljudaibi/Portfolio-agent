import chromadb
import json
import os
import PyPDF2

class PortfolioRAG:
    def __init__(self, persist_directory="./chroma_db"):
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection_name = "sarah_portfolio"
        self.collection = self._get_or_create_collection()
    
    def _get_or_create_collection(self):
        """Get existing collection or create new one"""
        try:
            collection = self.client.get_collection(name=self.collection_name)
            print(f"Found existing ChromaDB collection: {self.collection_name}")
            count = collection.count()
            if count == 0:
                print("Collection is empty, loading data...")
                self._load_all_data(collection)
            else:
                print(f"Collection has {count} documents")
            return collection
        except:
            print(f"Creating new ChromaDB collection: {self.collection_name}")
            collection = self.client.create_collection(name=self.collection_name)
            self._load_all_data(collection)
            return collection
    
    def _load_all_data(self, collection):
        """Load all portfolio data into ChromaDB"""
        print("Loading portfolio data...")
        self._load_resume_data(collection)
        self._load_json_portfolio(collection)
        self._load_github_data(collection)
        print("Portfolio data loaded successfully!")
    
    def _load_resume_data(self, collection):
        """Load resume PDF - for background, education, experience"""
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
                            documents=[f"Resume - Professional Background: {text}"],
                            metadatas=[{
                                "source": "resume",
                                "type": "background",
                                "filename": resume_file,
                                "content_type": "education_experience_summary"
                            }],
                            ids=[f"resume_{i}"]
                        )
                    print(f"Loaded resume: {resume_file}")
                except Exception as e:
                    print(f"Error loading {resume_file}: {e}")
        except Exception as e:
            print(f"Error loading resume data: {e}")
    
    def _load_json_portfolio(self, collection):
        """Load JSON portfolio data - projects and skills"""
        try:
            json_dir = 'data/json'
            if not os.path.exists(json_dir):
                print(f"JSON directory not found: {json_dir}")
                return
            
            # Load AI projects
            ai_projects_file = os.path.join(json_dir, 'AI_project.json')
            if os.path.exists(ai_projects_file):
                with open(ai_projects_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for record in data['records']:
                        doc_text = f"AI Project: {record['data'].get('Project Name', '')} - {record['data'].get('Description', '')} - Technologies: {record['data'].get('Key Technologies', '')}"
                        collection.add(
                            documents=[doc_text],
                            metadatas=[{
                                "source": "json_portfolio",
                                "type": "project",
                                "category": "ai_project",
                                "keywords": ','.join(record['metadata'].get('keywords', []))
                            }],
                            ids=[record['id']]
                        )
                print(f"Loaded {len(data['records'])} AI projects")
            
            # Load other projects
            other_projects_file = os.path.join(json_dir, 'other_projects.json')
            if os.path.exists(other_projects_file):
                with open(other_projects_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for record in data['records']:
                        doc_text = f"Project: {record['data'].get('Project Name', '')} - {record['data'].get('Description', '')} - Skills: {record['data'].get('Tech Skills', '')}"
                        collection.add(
                            documents=[doc_text],
                            metadatas=[{
                                "source": "json_portfolio",
                                "type": "project",
                                "category": "other_project",
                                "keywords": ','.join(record['metadata'].get('keywords', []))
                            }],
                            ids=[record['id']]
                        )
                print(f"Loaded {len(data['records'])} other projects")
            
            # Load skills
            skills_file = os.path.join(json_dir, 'skills_.json')
            if os.path.exists(skills_file):
                with open(skills_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for record in data['records']:
                        doc_text = f"Skills - {record['data'].get('Category', '')}: {record['data'].get('Skills', '')}"
                        collection.add(
                            documents=[doc_text],
                            metadatas=[{
                                "source": "json_portfolio",
                                "type": "skills",
                                "category": record['data'].get('Category', ''),
                                "keywords": ','.join(record['metadata'].get('keywords', []))
                            }],
                            ids=[record['id']]
                        )
                print(f"Loaded {len(data['records'])} skill categories")
                
        except Exception as e:
            print(f"Error loading JSON portfolio: {e}")
    
    def _load_github_data(self, collection):
        """Load GitHub profile and repository data"""
        try:
            # Load GitHub profile
            profile_path = 'data/github data/github_profile.json'
            if os.path.exists(profile_path):
                with open(profile_path, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
                    doc_text = f"GitHub Profile: {profile.get('name', 'N/A')} - Bio: {profile.get('bio', 'N/A')} - Location: {profile.get('location', 'N/A')} - Company: {profile.get('company', 'N/A')} - Public Repos: {profile.get('public_repos', 0)} - Followers: {profile.get('followers', 0)}"
                    collection.add(
                        documents=[doc_text],
                        metadatas=[{"source": "github", "type": "profile"}],
                        ids=["github_profile"]
                    )
                print("Loaded GitHub profile")
            
            # Load GitHub repositories
            repos_path = 'data/github data/github_repos.json'
            if os.path.exists(repos_path):
                with open(repos_path, 'r', encoding='utf-8') as f:
                    repos = json.load(f)
                    for i, repo in enumerate(repos):
                        doc_text = f"GitHub Repository: {repo['name']} - {repo.get('description', 'No description')} - Language: {repo.get('language', 'N/A')} - Stars: {repo.get('stars', 0)} - URL: {repo.get('url', '')}"
                        collection.add(
                            documents=[doc_text],
                            metadatas=[{
                                "source": "github",
                                "type": "repository",
                                "repo_name": repo['name'],
                                "language": repo.get('language', 'unknown') or 'unknown'
                            }],
                            ids=[f"github_repo_{i}"]
                        )
                print(f"Loaded {len(repos)} GitHub repositories")
            
            # Load GitHub README
            readme_path = 'data/github data/github_profile_readme.md'
            if os.path.exists(readme_path):
                with open(readme_path, 'r', encoding='utf-8') as f:
                    readme = f.read()
                    collection.add(
                        documents=[f"GitHub Profile README: {readme}"],
                        metadatas=[{"source": "github", "type": "readme"}],
                        ids=["github_readme"]
                    )
                print("Loaded GitHub README")
                    
        except Exception as e:
            print(f"Error loading GitHub data: {e}")
    
    def search(self, query, n_results=5):
        """Search portfolio data"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results
        except Exception as e:
            print(f"Search error: {e}")
            return {"documents": [[]], "metadatas": [[]]}
    
    def search_by_type(self, query, doc_type, n_results=10):
        """Search by document type"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where={"type": doc_type}
            )
            return results
        except:
            return {"documents": [[]], "metadatas": [[]]}
    
    def get_all_projects(self):
        """Get all projects"""
        try:
            results = self.collection.query(
                query_texts=["projects work"],
                n_results=50,
                where={"type": "project"}
            )
            return results
        except:
            return {"documents": [[]], "metadatas": [[]]}
    
    def get_all_skills(self):
        """Get all skills"""
        try:
            results = self.collection.query(
                query_texts=["skills technology"],
                n_results=50,
                where={"type": "skills"}
            )
            return results
        except:
            return {"documents": [[]], "metadatas": [[]]}
    
    def get_summary(self):
        """Get portfolio summary"""
        return "Sarah is a data scientist with expertise in AI, machine learning, and data analytics."
    
    def debug_search(self, query):
        """Debug search results"""
        try:
            print(f"\nSearching for: {query}")
            results = self.collection.query(query_texts=[query], n_results=5)
            print(f"Found {len(results['documents'][0])} results")
            for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
                print(f"{i+1}. {meta.get('type', 'unknown')}: {doc[:100]}...")
        except Exception as e:
            print(f"Debug error: {e}")
    
    def get_background_summary(self):
        """Get background info from resume"""
        try:
            results = self.collection.query(
                query_texts=["education experience work location years summary"],
                n_results=3,
                where={"type": "background"}
            )
            return results
        except:
            return {"documents": [[]], "metadatas": [[]]}
    
    def reload_data(self):
        """Reload all data"""
        try:
            self.client.delete_collection(name=self.collection_name)
        except:
            pass
        self.collection = self.client.create_collection(name=self.collection_name)
        self._load_all_data(self.collection)
