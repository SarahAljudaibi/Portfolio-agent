# Sarah Aljudaibi Portfolio

AI-powered portfolio assistant with video background.

## 🚀 Deploy to Render.com

### Step 1: Prepare Repository
1. Upload all files to GitHub repository
2. Include your video file in `static/` folder

### Step 2: Deploy on Render.com
1. Go to [render.com](https://render.com)
2. Sign up/Login with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: sarah-portfolio
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python flask_app.py`
6. Click "Create Web Service"

### Step 3: Access Your App
- Your app will be live at: `https://sarah-portfolio.onrender.com`
- First deployment takes 5-10 minutes

## 📁 Required Files
- `flask_app.py` - Main Flask application
- `portfolio_agent.py` - AI agent
- `portfolio_rag.py` - RAG system
- `templates/index.html` - Frontend
- `static/10339-865412856.mp4` - Video background
- `requirements.txt` - Dependencies
- `data/` - Portfolio data folder

## 🔧 Local Development
```bash
python flask_app.py
```
Visit: http://localhost:5000