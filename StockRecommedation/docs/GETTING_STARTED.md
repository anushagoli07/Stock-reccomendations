# Getting Started Guide

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Google Gemini API key
- Google Serper API key

## Installation Steps

### 1. Clone or Navigate to Project Directory

```bash
cd StockRecommedation
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env
```

The `.env` file has been created with default values. Edit it and add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
SERPER_API_KEY=your_serper_api_key_here
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
LOG_LEVEL=INFO
MODEL_NAME=gemini-2.5-flash
TEMPERATURE=0.7
MAX_TOKENS=2048
```

### 5. Get API Keys

#### Google Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

#### Google Serper API Key
1. Go to [Serper.dev](https://serper.dev)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Copy the key to your `.env` file

**Note:** The system uses Google Serper API for web search (requires SERPER_API_KEY).

## Running the Application

### Step 1: Start the Backend Server

Open a terminal and run:

```bash
cd backend
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Step 2: Start the Frontend

Open a **new terminal** (keep the backend running) and run:

```bash
streamlit run frontend/app.py
```

You should see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### Step 3: Use the Application

1. Open your browser and go to `http://localhost:8501`
2. Enter a stock symbol (e.g., "AAPL", "MSFT", "GOOGL")
3. Click "Analyze"
4. Wait for the analysis to complete (may take 1-3 minutes)
5. Review the results:
   - Stock information
   - Recommendations
   - Sentiment analysis
   - Detailed analysis
   - Recent news

## Troubleshooting

### Backend won't start

**Error:** `ModuleNotFoundError`
- **Solution:** Make sure all dependencies are installed: `pip install -r requirements.txt`

**Error:** `GEMINI_API_KEY not found`
- **Solution:** Check that your `.env` file exists and contains `GEMINI_API_KEY=your_key`

**Error:** Port 8000 already in use
- **Solution:** Change the port in `.env` or kill the process using port 8000

### Frontend can't connect to backend

**Error:** "API Not Available"
- **Solution:** Make sure the backend server is running on port 8000
- Check that `API_URL` in `frontend/app.py` matches your backend URL

### Analysis takes too long

- This is normal for the first run as agents need to gather data
- Subsequent analyses may be faster
- Consider adding caching for production use

### API Key Errors

**Error:** Invalid API key
- **Solution:** Verify your API key is correct in `.env`
- Make sure there are no extra spaces or quotes
- Regenerate the key if needed

## Testing the API Directly

You can test the API using curl or Postman:

```bash
# Health check
curl http://localhost:8000/health

# Analyze a stock
curl -X POST "http://localhost:8000/api/v1/analyze" \
     -H "Content-Type: application/json" \
     -d '{"stock_symbol": "AAPL"}'
```

Or use the interactive API docs at `http://localhost:8000/docs`

## Project Structure

```
StockRecommedation/
├── backend/           # FastAPI backend
├── frontend/          # Streamlit frontend
├── agents/            # LangGraph agents
├── config/            # Configuration
├── utils/             # Utilities
├── docs/              # Documentation
├── .env               # Environment variables (create this)
├── .env.example       # Example env file
├── requirements.txt   # Dependencies
└── README.md          # Main readme
```

## Next Steps

- Read [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture
- Customize agents in `agents/` directory
- Add new features to the frontend
- Extend API endpoints in `backend/api/routes.py`

## Support

For issues or questions:
1. Check the logs in the terminal
2. Review error messages in the UI
3. Check API documentation at `/docs` endpoint
4. Review the architecture documentation
