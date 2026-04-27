# Architecture Documentation

## System Overview

The Stock Recommendation System is an enterprise-level agentic AI application built with a client-server architecture. It uses LangChain and LangGraph to orchestrate multiple specialized agents that work together to provide comprehensive stock analysis and recommendations.

## Architecture Diagram

```
┌─────────────────┐
│  Streamlit UI   │  (Frontend)
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│  FastAPI Server │  (Backend)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Agent Service   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ LangGraph       │  (Orchestration)
│ Orchestrator    │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Extract │ │  News  │ │Analyze │ │Sentiment│ │Recommend│
│ Agent  │ │ Agent  │ │ Agent  │ │ Agent  │ │ Agent  │
└────────┘ └────────┘ └────────┘ └────────┘ └────────┘
    │         │          │          │          │
    └─────────┴──────────┴──────────┴──────────┘
                    │
                    ▼
            ┌───────────────┐
            │ Gemini 2.5   │
            │ Flash LLM    │
            └───────────────┘
                    │
                    ▼
            ┌───────────────┐
            │ Web Search    │
            │ (Google Serper)│
            └───────────────┘
```

## Component Details

### 1. Frontend (Streamlit)

**Location:** `frontend/app.py`

**Responsibilities:**
- User interface for stock symbol input
- Display of analysis results
- Visualization of sentiment and recommendations
- API communication with backend

**Features:**
- Modern, responsive UI
- Real-time analysis display
- Interactive charts and graphs
- News article browsing

### 2. Backend (FastAPI)

**Location:** `backend/`

**Components:**
- `main.py`: FastAPI application setup
- `api/routes.py`: API endpoint definitions
- `models/schemas.py`: Pydantic data models
- `services/agent_service.py`: Agent orchestration service

**API Endpoints:**
- `GET /health`: Health check
- `POST /api/v1/analyze`: Analyze stock and get recommendations

### 3. Agent System

**Location:** `agents/`

#### Base Agent (`base_agent.py`)
- Abstract base class for all agents
- Provides LLM initialization (Gemini 2.5 Flash)
- Tool management (web search, etc.)
- Common agent functionality

#### Stock Extraction Agent
- **Purpose:** Gathers real-time stock data from web sources
- **Input:** Stock symbol
- **Output:** Structured stock data (price, volume, metrics, etc.)
- **Tools:** Web search

#### News Aggregation Agent
- **Purpose:** Collects and filters relevant stock market news
- **Input:** Stock symbol, stock data
- **Output:** List of relevant news articles with summaries
- **Tools:** Web search

#### Stock Analysis Agent
- **Purpose:** Performs technical and fundamental analysis
- **Input:** Stock data, news articles
- **Output:** Comprehensive analysis (technical, fundamental, SWOT)
- **Tools:** LLM analysis

#### Sentiment Analysis Agent
- **Purpose:** Analyzes market sentiment from news and indicators
- **Input:** News articles, stock data
- **Output:** Sentiment scores and trends
- **Tools:** LLM analysis

#### Recommendation Agent
- **Purpose:** Generates actionable investment recommendations
- **Input:** All previous agent outputs
- **Output:** Investment recommendations with reasoning
- **Tools:** LLM analysis

### 4. Agent Orchestrator

**Location:** `agents/agent_orchestrator.py`

**Technology:** LangGraph

**Workflow:**
1. Extract Stock Data → 2. Aggregate News → 3. Analyze Stock → 4. Analyze Sentiment → 5. Generate Recommendations

**State Management:**
- Uses TypedDict for type-safe state
- Each agent updates the shared state
- Errors are collected and reported

## Data Flow

1. **User Input:** User enters stock symbol in Streamlit UI
2. **API Request:** Frontend sends POST request to `/api/v1/analyze`
3. **Agent Service:** Service initializes orchestrator and runs workflow
4. **Agent Execution:**
   - Extraction agent searches for stock data
   - News agent searches for relevant news
   - Analysis agent processes data and news
   - Sentiment agent analyzes sentiment
   - Recommendation agent generates final recommendations
5. **Response:** Results are returned to frontend
6. **Display:** UI displays formatted results

## Configuration

**Location:** `config/settings.py`

**Environment Variables:**
- `GEMINI_API_KEY`: Google Gemini API key (required)
- `BACKEND_HOST`: Backend server host
- `BACKEND_PORT`: Backend server port
- `LOG_LEVEL`: Logging level
- `MODEL_NAME`: LLM model name (default: gemini-2.5-flash)

## Error Handling

- Each agent handles errors gracefully
- Errors are collected in the workflow state
- API returns error details in response
- Frontend displays errors to users

## Scalability Considerations

- **Async Operations:** All agents use async/await for non-blocking operations
- **Stateless Design:** Backend is stateless, allowing horizontal scaling
- **Caching:** Can be added for frequently requested stocks
- **Rate Limiting:** Should be added for production use

## Security Considerations

- API keys stored in environment variables
- CORS configured (should be restricted in production)
- Input validation on API endpoints
- Error messages don't expose sensitive information

## Future Enhancements

- User authentication and session management
- Portfolio management features
- Real-time updates via WebSockets
- Multiple LLM provider support
