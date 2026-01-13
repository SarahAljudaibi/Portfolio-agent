from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

class ReasoningAgent:
    def __init__(self):
        # Set up Groq client
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        
    def analyze_and_respond(self, question, retrieved_data):
        """
        Takes retrieved data from RAG and uses reasoning to provide intelligent answers
        """
        if not retrieved_data or not any(doc.strip() for doc in retrieved_data):
            return self._no_data_response()
        
        # Create context from retrieved data
        context = "\n\n".join([doc for doc in retrieved_data if doc.strip()])
        
        # Generate reasoning-based response
        response = self._generate_intelligent_response(question, context)
        return response
    
    def _generate_intelligent_response(self, question, context):
        """Generate intelligent response using Groq"""
        try:
            system_prompt = """You are Sarah's intelligent portfolio assistant. Your job is to analyze the provided portfolio data and give thoughtful, well-reasoned responses.

RULES:
1. ONLY use information from the provided context
2. Analyze and synthesize the information intelligently
3. Provide structured, clear responses
4. If asked about projects, extract and organize them clearly
5. If asked about skills, categorize them (technical, soft skills, etc.)
6. If asked about experience, organize chronologically or by relevance
7. Always be professional but conversational
8. If information is incomplete, acknowledge it

RESPONSE FORMAT:
- Use bullet points for lists
- Organize information logically
- Provide brief explanations when helpful
- Keep responses concise but comprehensive"""

            user_prompt = f"""
Question: {question}

Portfolio Data:
{context}

Please analyze this data and provide a well-reasoned, organized response to the question."""

            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"I encountered an error while processing your question: {str(e)}"
    
    def _no_data_response(self):
        """Response when no relevant data is found"""
        return """I don't have that specific information in Sarah's portfolio data.

Here's what I can tell you about Sarah:

**Background:**
Sarah is a data scientist and AI enthusiast with experience in machine learning, data analysis, and Python programming.

**Key Projects:**
• Ryanair review analysis with AI-powered sentiment detection
• Time series forecasting for real estate valuation  
• Traffic accidents analysis in Saudi Arabia
• House prices prediction models

**Technical Skills:**
• Python programming
• Machine Learning & AI
• Data analysis and visualization
• Jupyter notebooks

For more detailed information, please contact Sarah directly:
📧 Email: sarahal.jodaiby@gmail.com
💼 LinkedIn: Connect with Sarah on LinkedIn"""

    def extract_projects(self, retrieved_data):
        """Specialized method to extract and organize projects"""
        if not retrieved_data:
            return "No project information found."
        
        context = "\n\n".join([doc for doc in retrieved_data if doc.strip()])
        
        try:
            system_prompt = """You are an expert at extracting and organizing project information. 
            
Extract all projects mentioned in the portfolio data and organize them clearly with:
1. Project name
2. Description/purpose
3. Technologies used
4. Key outcomes or features

Format as a clean, organized list."""

            user_prompt = f"""
Extract and organize all projects from this portfolio data:

{context}

Provide a well-structured list of Sarah's projects."""

            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=400,
                temperature=0.2
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error extracting projects: {str(e)}"
    
    def extract_skills(self, retrieved_data):
        """Specialized method to extract and categorize skills"""
        if not retrieved_data:
            return "No skills information found."
        
        context = "\n\n".join([doc for doc in retrieved_data if doc.strip()])
        
        try:
            system_prompt = """You are an expert at extracting and categorizing skills from portfolio data.

Extract all skills and organize them into categories:
- Programming Languages
- Technical Skills
- Tools & Frameworks
- Domain Expertise
- Soft Skills

Format as a clean, categorized list."""

            user_prompt = f"""
Extract and categorize all skills from this portfolio data:

{context}

Provide a well-organized breakdown of Sarah's skills by category."""

            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=400,
                temperature=0.2
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error extracting skills: {str(e)}"