# Stock Recommendation Agentic AI System

An enterprise-level agentic AI application that autonomously gathers, analyzes, and summarizes real-time stock market news and trends, providing actionable stock suggestions.

## Architecture

### Client-Server Architecture
- **Backend**: FastAPI server handling agent orchestration and API endpoints
- **Frontend**: Streamlit UI for user interaction and visualization
- **Agents**: LangGraph-based multi-agent system for stock analysis

### Agent System
1. **Stock Extraction Agent**: Gathers real-time stock data and news from web sources
2. **News Aggregation Agent**: Collects and filters relevant stock market news
3. **Stock Analysis Agent**: Analyzes stock performance, trends, and metrics
4. **Sentiment Analysis Agent**: Analyzes market sentiment from news and social media
5. **Stock Recommendation Agent**: Generates actionable investment recommendations

## Project Structure

```
StockRecommedation/
├── backend/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic models
│   └── services/
│       ├── __init__.py
│       └── agent_service.py    # Agent orchestration service
├── agents/
│   ├── __init__.py
│   ├── base_agent.py          # Base agent class
│   ├── stock_extraction_agent.py
│   ├── news_aggregation_agent.py
│   ├── stock_analysis_agent.py
│   ├── sentiment_analysis_agent.py
│   ├── recommendation_agent.py
│   └── agent_orchestrator.py  # LangGraph orchestration
├── config/
│   ├── __init__.py
│   └── settings.py            # Configuration management
├── utils/
│   ├── __init__.py
│   ├── logger.py              # Logging utilities
│   └── helpers.py             # Helper functions
├── frontend/
│   └── app.py                 # Streamlit application
├── .env.example               # Environment variables template
├── .env                       # Your environment variables (not in git)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Quick Start

### Prerequisites
- Python 3.9+
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Google Serper API key ([Get one here](https://serper.dev))

### Installation

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure Environment Variables**
   - Copy `.env.example` to `.env`
   - Add your API keys:
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` and add:
```env
GEMINI_API_KEY=your_gemini_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

**Note:** The system uses Google Serper API for web search (requires SERPER_API_KEY). The `.env` file has been created with default values.

3. **Run the Backend Server** (Terminal 1)
```bash
# Option 1: Using script (Windows)
run_backend.bat

# Option 2: Manual
cd backend
uvicorn main:app --reload --port 8000
```

4. **Run the Frontend** (Terminal 2)
```bash
# Option 1: Using script (Windows)
run_frontend.bat

# Option 2: Manual
streamlit run frontend/app.py
```

5. **Open Browser**
   - Frontend: http://localhost:8501
   - API Docs: http://localhost:8000/docs

## Usage

1. Start the FastAPI backend server
2. Start the Streamlit frontend
3. Enter a stock symbol (e.g., "AAPL", "MSFT") in the UI
4. The system will:
   - Extract real-time stock data
   - Gather relevant news
   - Analyze stock performance
   - Analyze market sentiment
   - Generate recommendations

## API Endpoints

### POST /api/v1/analyze
Analyze a stock and get recommendations.

**Request Body:**
```json
{
  "stock_symbol": "AAPL"
}
```

**Response:**
```json
{
  "stock_symbol": "AAPL",
  "stock_data": {...},
  "news": [...],
  "analysis": {...},
  "sentiment": {...},
  "recommendations": [...]
}
```

## Technology Stack

- **LLM**: Google Gemini 2.5 Flash (configurable)
- **Framework**: LangChain + LangGraph
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Web Search**: Google Serper API (requires SERPER_API_KEY)
- **Visualization**: Plotly

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[Getting Started Guide](docs/GETTING_STARTED.md)** - Detailed setup and installation instructions
- **[Architecture Documentation](docs/ARCHITECTURE.md)** - System architecture and design
- **[Agent Details](docs/AGENT_DETAILS.md)** - Detailed information about each agent
- **[API Documentation](docs/API_DOCUMENTATION.md)** - Complete API reference

## Development

### Adding New Agents
1. Create a new agent class in `agents/` inheriting from `BaseAgent`
2. Implement the required methods
3. Register the agent in `agents/agent_orchestrator.py`

### Extending Functionality
- Add new tools in `agents/base_agent.py`
- Extend API endpoints in `backend/api/routes.py`
- Update UI components in `frontend/app.py`

## Features

✅ **Multi-Agent System**: 5 specialized agents working together  
✅ **Real-time Data**: Web search integration for current stock information  
✅ **Comprehensive Analysis**: Technical, fundamental, and sentiment analysis  
✅ **Actionable Recommendations**: Detailed investment recommendations with entry/exit strategies  
✅ **Modern UI**: Beautiful Streamlit interface with interactive visualizations  
✅ **Enterprise Architecture**: Clean separation of concerns, scalable design  
✅ **Web Search**: Uses Google Serper API for comprehensive search results  
✅ **Error Handling**: Robust error handling and logging  
✅ **Documentation**: Comprehensive documentation for developers  

## Support

For issues or questions:
- Check the [Getting Started Guide](docs/GETTING_STARTED.md)
- Review the [Architecture Documentation](docs/ARCHITECTURE.md)
- Check API documentation at `/docs` endpoint when server is running
