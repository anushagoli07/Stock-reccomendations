# API Documentation

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health Check

**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "Stock Recommendation API is running"
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

---

### Analyze Stock

**POST** `/api/v1/analyze`

Analyze a stock and get comprehensive recommendations.

**Request Body:**
```json
{
  "stock_symbol": "AAPL"
}
```

**Parameters:**
- `stock_symbol` (string, required): Stock symbol to analyze (e.g., "AAPL", "MSFT", "GOOGL")

**Response:**
```json
{
  "stock_symbol": "AAPL",
  "stock_data": {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "price": 175.50,
    "change": 2.30,
    "change_percent": 1.33,
    "volume": 50000000,
    "market_cap": 2800000000000,
    "pe_ratio": 28.5,
    "dividend_yield": 0.5,
    "sector": "Technology",
    "industry": "Consumer Electronics"
  },
  "news_articles": [
    {
      "title": "Apple Reports Strong Q4 Earnings",
      "source": "Reuters",
      "url": "https://...",
      "published_date": "2024-01-15",
      "summary": "Apple reported better than expected earnings...",
      "relevance_score": 0.95,
      "sentiment": "positive"
    }
  ],
  "analysis": {
    "technical_analysis": {
      "trend": "bullish",
      "support_level": 170.0,
      "resistance_level": 180.0,
      "momentum": "strong",
      "volatility": "medium"
    },
    "fundamental_analysis": {
      "valuation": "fair",
      "financial_health": "strong",
      "growth_prospects": "good",
      "competitive_position": "strong"
    },
    "risk_assessment": {
      "overall_risk": "medium",
      "market_risk": "medium",
      "company_specific_risk": "low",
      "risk_factors": []
    },
    "key_insights": [
      "Strong financial position",
      "Innovation leadership"
    ],
    "strengths": ["Brand value", "Cash reserves"],
    "weaknesses": ["Market saturation"],
    "opportunities": ["New markets"],
    "threats": ["Competition"]
  },
  "sentiment": {
    "overall_sentiment": "positive",
    "sentiment_score": 0.65,
    "news_sentiment": {
      "positive_count": 8,
      "negative_count": 2,
      "neutral_count": 5,
      "average_sentiment": 0.6
    },
    "market_sentiment": {
      "investor_sentiment": "bullish",
      "analyst_sentiment": "positive",
      "retail_sentiment": "positive"
    },
    "key_sentiment_drivers": [
      "Strong earnings",
      "Product launches"
    ],
    "sentiment_trend": "improving",
    "confidence_level": 0.8
  },
  "recommendations": {
    "primary_recommendation": {
      "action": "BUY",
      "confidence": 0.75,
      "target_price": 185.0,
      "time_horizon": "medium_term",
      "reasoning": "Strong fundamentals and positive sentiment...",
      "risk_level": "medium"
    },
    "alternative_scenarios": [
      {
        "scenario": "Market correction",
        "action": "HOLD",
        "probability": 0.3,
        "target_price": 170.0,
        "reasoning": "If market corrects, hold position"
      }
    ],
    "key_factors": [
      "Strong financials",
      "Positive sentiment",
      "Market position"
    ],
    "entry_strategy": {
      "recommended_entry_price": 175.0,
      "entry_timing": "immediate",
      "position_sizing": "medium",
      "stop_loss": 165.0
    },
    "exit_strategy": {
      "take_profit_targets": [
        {"price": 185.0, "percentage": 50},
        {"price": 195.0, "percentage": 50}
      ],
      "exit_conditions": [
        "Target price reached",
        "Stop loss triggered"
      ]
    },
    "portfolio_considerations": {
      "sector_allocation": "Consider tech sector exposure",
      "diversification": "Good diversification",
      "correlation": "Low correlation with holdings"
    }
  },
  "errors": []
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
     -H "Content-Type: application/json" \
     -d '{"stock_symbol": "AAPL"}'
```

**Status Codes:**
- `200 OK`: Analysis completed successfully
- `400 Bad Request`: Invalid request (missing stock_symbol)
- `500 Internal Server Error`: Server error during analysis

**Notes:**
- Analysis may take 1-3 minutes to complete
- The endpoint is asynchronous and will wait for all agents to complete
- Errors from individual agents are collected and returned in the `errors` field

---

## Interactive API Documentation

FastAPI provides interactive API documentation at:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

You can test endpoints directly from these interfaces.

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message description"
}
```

## Rate Limiting

Currently, there is no rate limiting implemented. For production use, consider adding:
- Rate limiting per IP
- Rate limiting per API key
- Request queuing for high load

## Authentication

Currently, the API does not require authentication. For production use, consider:
- API key authentication
- OAuth 2.0
- JWT tokens

## CORS

CORS is currently configured to allow all origins (`*`). For production:
- Restrict to specific frontend domains
- Configure proper CORS headers
- Handle preflight requests
