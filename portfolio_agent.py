from portfolio_rag import PortfolioRAG

class PortfolioAgent:
    def __init__(self):
        self.rag = PortfolioRAG()
        self.email = "sarahal.jodaiby@gmail.com"
        self.linkedin = "LinkedIn profile"
    
    def answer_question(self, question):
        """Answer questions using only portfolio data"""
        # Search for relevant information
        search_results = self.rag.search(question, n_results=3)
        
        # Check if we found relevant information
        if not search_results['documents'][0] or not any(doc.strip() for doc in search_results['documents'][0]):
            return self._no_info_response()
        
        # Combine relevant documents
        context = "\n\n".join([doc for doc in search_results['documents'][0] if doc.strip()])
        
        # Generate response based on context
        response = self._generate_response(question, context)
        return response
    
    def _no_info_response(self):
        """Response when information is not available"""
        summary = self.rag.get_summary()
        
        response = f"""I don't have that information in Sarah's portfolio data.

Here's a summary about Sarah:
{summary}

For more detailed information, you can contact Sarah at:
📧 Email: {self.email}
💼 LinkedIn: Connect with her on LinkedIn

Feel free to reach out directly for any specific questions!"""
        
        return response
    
    def _generate_response(self, question, context):
        """Generate response using only the provided context"""
        question_lower = question.lower()
        
        # Determine response type based on question
        if any(word in question_lower for word in ["experience", "work", "job", "career"]):
            return f"Based on Sarah's portfolio data:\n\n{context}"
        
        elif any(word in question_lower for word in ["skills", "technology", "programming", "tools"]):
            return f"Sarah's technical skills and technologies:\n\n{context}"
        
        elif any(word in question_lower for word in ["projects", "github", "repository", "code"]):
            return f"Sarah's projects and GitHub work:\n\n{context}"
        
        elif any(word in question_lower for word in ["education", "degree", "university", "study"]):
            return f"Sarah's educational background:\n\n{context}"
        
        elif any(word in question_lower for word in ["about", "who", "background", "bio"]):
            return f"About Sarah:\n\n{context}"
        
        elif any(word in question_lower for word in ["contact", "email", "reach", "linkedin"]):
            return f"Contact Information:\n📧 Email: {self.email}\n💼 LinkedIn: Connect with Sarah on LinkedIn\n\nAdditional info from portfolio:\n{context}"
        
        else:
            return f"Here's what I found in Sarah's portfolio:\n\n{context}"
    
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