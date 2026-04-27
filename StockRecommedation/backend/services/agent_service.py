"""Service for orchestrating agent workflows."""

from typing import Dict, Any
from agents.agent_orchestrator import AgentOrchestrator
from utils.logger import logger


class AgentService:
    """Service for managing agent operations."""
    
    def __init__(self):
        """Initialize the agent service."""
        self.orchestrator = AgentOrchestrator()
        logger.info("Agent service initialized")
    
    async def analyze_stock(self, stock_symbol: str) -> Dict[str, Any]:
        """Analyze a stock using the agent workflow.
        
        Args:
            stock_symbol: Stock symbol to analyze
            
        Returns:
            Complete analysis results
        """
        logger.info(f"Service: Analyzing stock {stock_symbol}")
        try:
            result = await self.orchestrator.run(stock_symbol)
            return result
        except Exception as e:
            logger.error(f"Service error analyzing {stock_symbol}: {str(e)}")
            return {
                "stock_symbol": stock_symbol,
                "error": str(e),
                "errors": [str(e)]
            }
