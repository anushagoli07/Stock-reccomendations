"""API routes for the stock analysis service."""

from fastapi import APIRouter, HTTPException, status
from backend.models.schemas import (
    StockAnalysisRequest,
    StockAnalysisResponse,
    HealthResponse
)
from backend.services.agent_service import AgentService
from utils.logger import logger

router = APIRouter()
agent_service = AgentService()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        message="Stock Recommendation API is running"
    )


@router.post("/api/v1/analyze", response_model=StockAnalysisResponse)
async def analyze_stock(request: StockAnalysisRequest):
    """Analyze a stock and return comprehensive recommendations.
    
    Args:
        request: Stock analysis request containing stock symbol
        
    Returns:
        Complete stock analysis with recommendations
    """
    stock_symbol = request.stock_symbol.strip().upper()
    
    if not stock_symbol:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stock symbol is required"
        )
    
    logger.info(f"API: Received analysis request for {stock_symbol}")
    
    try:
        result = await agent_service.analyze_stock(stock_symbol)
        
        # Convert to response model
        response = StockAnalysisResponse(
            stock_symbol=result.get("stock_symbol", stock_symbol),
            stock_data=result.get("stock_data"),
            news_articles=result.get("news_articles", []),
            analysis=result.get("analysis"),
            sentiment=result.get("sentiment"),
            recommendations=result.get("recommendations"),
            errors=result.get("errors", [])
        )
        
        return response
        
    except Exception as e:
        logger.error(f"API error analyzing {stock_symbol}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing stock: {str(e)}"
        )
