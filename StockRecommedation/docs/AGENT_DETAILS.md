# Agent Details Documentation

## Overview

The system uses 5 specialized agents that work together in a LangGraph orchestrated workflow. Each agent has a specific responsibility and contributes to the final recommendation.

## Agent Workflow

```
Stock Symbol Input
    ↓
[1] Stock Extraction Agent
    ↓
[2] News Aggregation Agent
    ↓
[3] Stock Analysis Agent
    ↓
[4] Sentiment Analysis Agent
    ↓
[5] Recommendation Agent
    ↓
Final Recommendations
```

## Agent Descriptions

### 1. Stock Extraction Agent

**Purpose:** Gathers real-time stock data from web sources

**Input:**
- Stock symbol (e.g., "AAPL")

**Output:**
- Structured stock data including:
  - Current price
  - Price change and percentage
  - Trading volume
  - Market capitalization
  - P/E ratio
  - Dividend yield
  - 52-week high/low
  - Sector and industry information

**Tools Used:**
- Web search (Tavily or fallback)
- LLM for data extraction and structuring

**Key Features:**
- Extracts data from multiple web sources
- Structures unstructured data into JSON format
- Handles missing data gracefully

### 2. News Aggregation Agent

**Purpose:** Collects and filters relevant stock market news

**Input:**
- Stock symbol
- Stock data (from previous agent)

**Output:**
- List of relevant news articles with:
  - Title
  - Source
  - URL
  - Publication date
  - Summary
  - Relevance score
  - Sentiment (positive/negative/neutral)

**Tools Used:**
- Web search for news articles
- LLM for filtering and summarization

**Key Features:**
- Filters news by relevance
- Summarizes articles
- Scores articles by importance
- Returns top 10 most relevant articles

### 3. Stock Analysis Agent

**Purpose:** Performs comprehensive technical and fundamental analysis

**Input:**
- Stock symbol
- Stock data
- News articles

**Output:**
- Technical analysis:
  - Trend (bullish/bearish/neutral)
  - Support and resistance levels
  - Momentum indicators
  - Volatility assessment
- Fundamental analysis:
  - Valuation assessment
  - Financial health
  - Growth prospects
  - Competitive position
- Risk assessment:
  - Overall risk level
  - Market risk
  - Company-specific risk
  - Risk factors
- SWOT analysis:
  - Strengths
  - Weaknesses
  - Opportunities
  - Threats
- Key insights

**Tools Used:**
- LLM for comprehensive analysis

**Key Features:**
- Multi-dimensional analysis
- Risk assessment
- SWOT framework
- Actionable insights

### 4. Sentiment Analysis Agent

**Purpose:** Analyzes market sentiment from news and indicators

**Input:**
- Stock symbol
- News articles
- Stock data

**Output:**
- Overall sentiment (very positive to very negative)
- Sentiment score (-1 to 1)
- News sentiment breakdown:
  - Positive/negative/neutral article counts
  - Average sentiment
- Market sentiment:
  - Investor sentiment
  - Analyst sentiment
  - Retail sentiment
- Key sentiment drivers
- Sentiment trend (improving/declining/stable)
- Confidence level

**Tools Used:**
- LLM for sentiment analysis

**Key Features:**
- Multi-source sentiment analysis
- Trend identification
- Confidence scoring
- Driver identification

### 5. Recommendation Agent

**Purpose:** Generates actionable investment recommendations

**Input:**
- All previous agent outputs:
  - Stock data
  - News articles
  - Analysis
  - Sentiment

**Output:**
- Primary recommendation:
  - Action (STRONG_BUY/BUY/HOLD/SELL/STRONG_SELL)
  - Confidence score (0 to 1)
  - Target price
  - Time horizon
  - Detailed reasoning
  - Risk level
- Alternative scenarios:
  - Different market scenarios
  - Probability of each scenario
  - Actions for each scenario
- Key factors influencing recommendation
- Entry strategy:
  - Recommended entry price
  - Entry timing
  - Position sizing
  - Stop loss levels
- Exit strategy:
  - Take profit targets
  - Exit conditions
- Portfolio considerations:
  - Sector allocation impact
  - Diversification impact
  - Correlation with existing holdings

**Tools Used:**
- LLM for recommendation generation

**Key Features:**
- Actionable recommendations
- Multiple scenario planning
- Entry/exit strategies
- Portfolio integration

## Agent Communication

Agents communicate through a shared state managed by LangGraph:

```python
class AgentState(TypedDict):
    stock_symbol: str
    stock_data: Dict[str, Any]
    news_articles: list
    analysis: Dict[str, Any]
    sentiment: Dict[str, Any]
    recommendations: Dict[str, Any]
    errors: list
```

Each agent:
1. Reads relevant data from state
2. Performs its analysis
3. Updates state with results
4. Passes control to next agent

## Error Handling

Each agent implements error handling:
- Catches exceptions during execution
- Logs errors for debugging
- Returns error status in output
- Allows workflow to continue even if one agent fails

## Extending Agents

To add a new agent:

1. Create a new agent class in `agents/`:
```python
from agents.base_agent import BaseAgent

class NewAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="New Agent",
            description="Agent description"
        )
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation
        pass
```

2. Add agent to orchestrator in `agents/agent_orchestrator.py`
3. Add node to workflow graph
4. Connect to workflow edges

## Performance Considerations

- Agents run sequentially (can be parallelized for independent agents)
- Each agent makes LLM calls (may take 10-30 seconds each)
- Total analysis time: 1-3 minutes typically
- Consider caching for frequently analyzed stocks

## Best Practices

1. **Clear Input/Output:** Each agent should have well-defined inputs and outputs
2. **Error Handling:** Always handle errors gracefully
3. **Logging:** Log important steps for debugging
4. **Idempotency:** Agents should produce consistent results for same inputs
5. **Modularity:** Keep agents focused on single responsibilities
