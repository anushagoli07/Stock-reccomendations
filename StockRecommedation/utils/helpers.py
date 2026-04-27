"""Helper utility functions."""

from typing import Dict, Any, List
from datetime import datetime


def format_stock_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Format stock data for display.
    
    Args:
        data: Raw stock data dictionary
        
    Returns:
        Formatted stock data
    """
    formatted = {
        "symbol": data.get("symbol", ""),
        "name": data.get("name", ""),
        "price": data.get("price", 0.0),
        "change": data.get("change", 0.0),
        "change_percent": data.get("change_percent", 0.0),
        "volume": data.get("volume", 0),
        "market_cap": data.get("market_cap", ""),
        "timestamp": datetime.now().isoformat()
    }
    return formatted


def format_recommendations(recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Format recommendations for display.
    
    Args:
        recommendations: List of recommendation dictionaries
        
    Returns:
        Formatted recommendations
    """
    formatted = []
    for rec in recommendations:
        formatted.append({
            "action": rec.get("action", "HOLD"),
            "confidence": rec.get("confidence", 0.0),
            "reasoning": rec.get("reasoning", ""),
            "target_price": rec.get("target_price", None),
            "time_horizon": rec.get("time_horizon", "N/A")
        })
    return formatted
