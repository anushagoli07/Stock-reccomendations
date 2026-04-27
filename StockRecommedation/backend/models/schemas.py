"""Pydantic schemas for API request/response models."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class StockAnalysisRequest(BaseModel):
    """Request model for stock analysis."""
    stock_symbol: str = Field(..., description="Stock symbol to analyze (e.g., AAPL, MSFT)")


class StockData(BaseModel):
    """Stock data model."""
    symbol: str
    name: Optional[str] = None
    price: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    volume: Optional[int] = None
    market_cap: Optional[str] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None


class NewsArticle(BaseModel):
    """News article model."""
    title: str
    source: Optional[str] = None
    url: Optional[str] = None
    published_date: Optional[str] = None
    summary: Optional[str] = None
    relevance_score: Optional[float] = None
    sentiment: Optional[str] = None


class TechnicalAnalysis(BaseModel):
    """Technical analysis model."""
    trend: Optional[str] = None
    support_level: Optional[float] = None
    resistance_level: Optional[float] = None
    momentum: Optional[str] = None
    volatility: Optional[str] = None


class FundamentalAnalysis(BaseModel):
    """Fundamental analysis model."""
    valuation: Optional[str] = None
    financial_health: Optional[str] = None
    growth_prospects: Optional[str] = None
    competitive_position: Optional[str] = None


class RiskAssessment(BaseModel):
    """Risk assessment model."""
    overall_risk: Optional[str] = None
    market_risk: Optional[str] = None
    company_specific_risk: Optional[str] = None
    risk_factors: Optional[List[str]] = None


class StockAnalysis(BaseModel):
    """Stock analysis model."""
    technical_analysis: Optional[TechnicalAnalysis] = None
    fundamental_analysis: Optional[FundamentalAnalysis] = None
    risk_assessment: Optional[RiskAssessment] = None
    key_insights: Optional[List[str]] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    opportunities: Optional[List[str]] = None
    threats: Optional[List[str]] = None


class Sentiment(BaseModel):
    """Sentiment analysis model."""
    overall_sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    news_sentiment: Optional[Dict[str, Any]] = None
    market_sentiment: Optional[Dict[str, Any]] = None
    key_sentiment_drivers: Optional[List[str]] = None
    sentiment_trend: Optional[str] = None
    confidence_level: Optional[float] = None


class Recommendation(BaseModel):
    """Stock recommendation model."""
    action: Optional[str] = None
    confidence: Optional[float] = None
    target_price: Optional[float] = None
    time_horizon: Optional[str] = None
    reasoning: Optional[str] = None
    risk_level: Optional[str] = None


class StockRecommendations(BaseModel):
    """Complete recommendations model."""
    primary_recommendation: Optional[Recommendation] = None
    alternative_scenarios: Optional[List[Dict[str, Any]]] = None
    key_factors: Optional[List[str]] = None
    entry_strategy: Optional[Dict[str, Any]] = None
    exit_strategy: Optional[Dict[str, Any]] = None
    portfolio_considerations: Optional[Dict[str, Any]] = None


class StockAnalysisResponse(BaseModel):
    """Response model for stock analysis."""
    stock_symbol: str
    stock_data: Optional[StockData] = None
    news_articles: Optional[List[NewsArticle]] = None
    analysis: Optional[StockAnalysis] = None
    sentiment: Optional[Sentiment] = None
    recommendations: Optional[StockRecommendations] = None
    errors: Optional[List[str]] = None


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    message: str
