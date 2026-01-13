from portfolio_rag import PortfolioRAG
from reasoning_agent import ReasoningAgent

class PortfolioAgent:
    def __init__(self):
        self.rag = PortfolioRAG()
        self.reasoning_agent = ReasoningAgent()
        self.email = "sarahal.jodaiby@gmail.com"
        self.linkedin = "https://www.linkedin.com/in/sarah-aljudaibi/"
    
    def answer_question(self, question):
        """Main method: RAG retrieves data, Reasoning Agent processes it"""
        # Step 1: Retrieve relevant data using RAG
        search_results = self.rag.search(question, n_results=5)
        
        # Step 2: Extract documents from search results
        retrieved_docs = []
        if search_results['documents'][0]:
            retrieved_docs = search_results['documents'][0]
        
        # Step 3: Use Reasoning Agent to analyze and respond
        if self._is_projects_question(question):
            response = self.reasoning_agent.extract_projects(retrieved_docs)
        elif self._is_skills_question(question):
            response = self.reasoning_agent.extract_skills(retrieved_docs)
        else:
            response = self.reasoning_agent.analyze_and_respond(question, retrieved_docs)
        
        return response
    
    def _is_projects_question(self, question):
        """Check if question is about projects"""
        project_keywords = ['project', 'projects', 'work', 'portfolio', 'github', 'repository', 'built', 'developed']
        return any(keyword in question.lower() for keyword in project_keywords)
    
    def _is_skills_question(self, question):
        """Check if question is about skills"""
        skill_keywords = ['skill', 'skills', 'technology', 'technologies', 'programming', 'language', 'tool', 'framework']
        return any(keyword in question.lower() for keyword in skill_keywords)
    
    def chat(self):
        """Interactive chat interface"""
        print("\n" + "="*50)
        print("🤖 Sarah's Portfolio Assistant")
        print("="*50)
        print("Ask me anything about Sarah's background, skills, projects, or experience!")
        print("Type 'quit', 'exit', or 'bye' to end the conversation")
        print("Type 'reload' to refresh the data")
        print("-"*50 + "\n")
        
        while True:
            try:
                question = input("You: ").strip()
                
                if not question:
                    continue
                    
                if question.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Thank you for using Sarah's Portfolio Assistant! Goodbye!")
                    break
                
                if question.lower() == 'reload':
                    print("🔄 Reloading portfolio data...")
                    self.rag.reload_data()
                    print("✅ Data reloaded successfully!")
                    continue
                
                print("\n🤖 Assistant:", end=" ")
                answer = self.answer_question(question)
                print(f"{answer}\n")
                print("-"*50)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Sorry, I encountered an error: {e}")
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