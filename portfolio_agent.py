from portfolio_rag import PortfolioRAG
from reasoning_agent import ReasoningAgent

class PortfolioAgent:
    def __init__(self):
        self.rag = PortfolioRAG()
        self.reasoning_agent = ReasoningAgent()
        self.email = "sarahal.jodaiby@gmail.com"
        self.linkedin = "https://www.linkedin.com/in/sarah-aljudaibi/"
    
    def answer_question(self, question, history=None):
        """Enhanced question answering with progressive retrieval"""
        history = history or []
        # Step 1: Detect intent and use appropriate retrieval strategy
        intent = self._detect_intent(question)
        
        # Step 2: Progressive retrieval based on intent
        if intent == "projects":
            search_results = self._get_projects_data(question)
        elif intent == "skills":
            search_results = self._get_skills_data(question)
        elif intent == "skills_specific":
            search_results = self._get_skills_data(question)
        elif intent == "github":
            search_results = self._get_github_data(question)
        elif intent == "experience":
            search_results = self._get_experience_data(question)
        else:
            # General search with enhanced retrieval
            search_results = self.rag.search(question, n_results=8)
        
        # Step 3: Extract documents from search results
        retrieved_docs = []
        if search_results and search_results.get('documents') and search_results['documents'][0]:
            retrieved_docs = search_results['documents'][0]
        
        # Step 4: Fallback if no relevant docs found
        if not retrieved_docs:
            retrieved_docs = self._fallback_retrieval(question)
        
        # Step 5: Use Reasoning Agent to analyze and respond
        if intent == "projects":
            response = self.reasoning_agent.extract_projects(retrieved_docs, history)
        elif intent == "skills":
            response = self.reasoning_agent.extract_skills(retrieved_docs, history, question=None)
        elif intent == "skills_specific":
            response = self.reasoning_agent.extract_skills(retrieved_docs, history, question=question)
        else:
            response = self.reasoning_agent.analyze_and_respond(question, retrieved_docs, history)
        
        # Step 6: Add contact info if relevant
        if self._should_add_contact(question):
            response += f"\n\n📧 Contact: {self.email}\n🔗 LinkedIn: {self.linkedin}"
        
        return response
    
    def _detect_intent(self, question):
        """Soft intent detection (not hard routing)"""
        question_lower = question.lower()
        
        # Project-related keywords
        project_keywords = ['project', 'projects', 'work', 'portfolio', 'built', 'developed', 'created', 'github', 'repository', 'repo']
        if any(keyword in question_lower for keyword in project_keywords):
            if any(word in question_lower for word in ['github', 'repository', 'repo']):
                return "github"
            return "projects"
        
        # Specific tool/library/domain names — route to focused skill lookup
        specific_tool_keywords = [
            'python', 'sql', 'html', 'css', 'javascript', 'bootstrap',
            'pytorch', 'tensorflow', 'keras', 'scikit', 'sklearn', 'hugging face', 'huggingface',
            'openai', 'groq', 'ollama', 'yolo', 'ultralytics',
            'pandas', 'numpy', 'opencv', 'matplotlib', 'seaborn', 'plotly',
            'power bi', 'tableau', 'flask', 'streamlit', 'render',
            'jupyter', 'colab', 'aws', 'visual studio',
            'nlp', 'llm', 'generative ai', 'gen ai', 'large language',
            'classification', 'regression', 'forecasting', 'computer vision',
            'etl', 'web scraping', 'api', 'data cleaning', 'data processing'
        ]
        if any(keyword in question_lower for keyword in specific_tool_keywords):
            return "skills_specific"

        # Generic skills question
        generic_skill_keywords = ['skill', 'skills', 'technology', 'technologies', 'programming', 'language', 'tool', 'framework', 'technical']
        if any(keyword in question_lower for keyword in generic_skill_keywords):
            return "skills"
        
        # Experience-related keywords
        experience_keywords = ['experience', 'background', 'resume', 'education', 'career', 'history']
        if any(keyword in question_lower for keyword in experience_keywords):
            return "experience"
        
        return "general"
    
    def _get_projects_data(self, question):
        """Get project data with multiple strategies"""
        # Strategy 1: Direct project search
        results = self.rag.search_by_type(question, "project", 6)
        
        # Strategy 2: If insufficient results, get all projects
        if not results['documents'][0] or len(results['documents'][0]) < 3:
            all_projects = self.rag.get_all_projects()
            if all_projects['documents'][0]:
                return all_projects
        
        # Strategy 3: Fallback to general search
        if not results['documents'][0]:
            return self.rag.search(f"projects work {question}", n_results=8)
        
        return results
    
    def _get_skills_data(self, question):
        """Get skills data with multiple strategies"""
        # Strategy 1: Direct skills search
        results = self.rag.search_by_type(question, "skills", 6)
        
        # Strategy 2: If insufficient results, get all skills
        if not results['documents'][0] or len(results['documents'][0]) < 2:
            all_skills = self.rag.get_all_skills()
            if all_skills['documents'][0]:
                return all_skills
        
        # Strategy 3: Fallback to general search
        if not results['documents'][0]:
            return self.rag.search(f"skills technology {question}", n_results=8)
        
        return results
    
    def _get_github_data(self, question):
        """Get GitHub-specific data"""
        # Search for GitHub repositories and profile
        github_results = self.rag.search(question, n_results=10)
        
        # Filter for GitHub-related content
        if github_results['documents'][0]:
            filtered_docs = []
            filtered_metas = []
            
            for doc, meta in zip(github_results['documents'][0], github_results['metadatas'][0]):
                if meta.get('source', '').startswith('github') or 'github' in doc.lower():
                    filtered_docs.append(doc)
                    filtered_metas.append(meta)
            
            if filtered_docs:
                return {'documents': [filtered_docs], 'metadatas': [filtered_metas]}
        
        # Fallback to general search
        return self.rag.search(f"github repository {question}", n_results=8)
    
    def _get_experience_data(self, question):
        """Get experience and background data"""
        # Search for resume and background information
        results = self.rag.search(question, n_results=8)
        
        # Prioritize formal background documents
        if results['documents'][0]:
            prioritized_docs = []
            prioritized_metas = []
            other_docs = []
            other_metas = []
            
            for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
                if meta.get('type') in ['formal_background', 'personal_background']:
                    prioritized_docs.append(doc)
                    prioritized_metas.append(meta)
                else:
                    other_docs.append(doc)
                    other_metas.append(meta)
            
            # Combine prioritized first, then others
            final_docs = prioritized_docs + other_docs[:5]
            final_metas = prioritized_metas + other_metas[:5]
            
            return {'documents': [final_docs], 'metadatas': [final_metas]}
        
        return results
    
    def _fallback_retrieval(self, question):
        """Fallback when no relevant documents found"""
        # Try broader search terms
        fallback_queries = [
            "Sarah portfolio projects skills",
            "data science machine learning",
            "programming experience background"
        ]
        
        for fallback_query in fallback_queries:
            results = self.rag.search(fallback_query, n_results=5)
            if results['documents'][0]:
                return results['documents'][0]
        
        # Last resort: return summary
        return [self.rag.get_summary()]
    
    def _should_add_contact(self, question):
        """Check if contact info should be added"""
        contact_keywords = ['contact', 'email', 'reach', 'linkedin', 'connect', 'hire', 'work']
        return any(keyword in question.lower() for keyword in contact_keywords)
    
    def chat(self):
        """Interactive chat interface"""
        print("\n" + "="*50)
        print("Sarah's Portfolio Assistant")
        print("="*50)
        print("Ask me anything about Sarah's background, skills, projects, or experience!")
        print("Type 'quit', 'exit', or 'bye' to end the conversation")
        print("Type 'reload' to refresh the data")
        print("Type 'debug <query>' to see search results")
        print("-"*50 + "\n")
        
        while True:
            try:
                question = input("You: ").strip()
                
                if not question:
                    continue
                    
                if question.lower() in ['quit', 'exit', 'bye']:
                    print("\nGoodbye!")
                    break
                
                if question.lower() == 'reload':
                    print("Reloading portfolio data...")
                    self.rag.reload_data()
                    print("Data reloaded successfully!")
                    continue
                
                if question.lower().startswith('debug '):
                    debug_query = question[6:].strip()
                    self.rag.debug_search(debug_query)
                    continue
                
                print("\nAssistant:", end=" ")
                answer = self.answer_question(question)
                print(f"{answer}\n")
                print("-"*50)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nSorry, I encountered an error: {e}")
                print("Please try asking your question again.\n")

def main():
    """Main function to run the portfolio agent"""
    try:
        agent = PortfolioAgent()
        agent.chat()
    except Exception as e:
        print(f"Error starting the agent: {e}")
        print("Please make sure all required files are in place and try again.")

if __name__ == "__main__":
    main()