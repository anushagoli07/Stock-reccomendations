"""LangGraph-based agent orchestrator for coordinating multiple agents."""

from typing import Dict, Any, TypedDict
from langgraph.graph import StateGraph, END
from agents.stock_extraction_agent import StockExtractionAgent
from agents.news_aggregation_agent import NewsAggregationAgent
from agents.stock_analysis_agent import StockAnalysisAgent
from agents.sentiment_analysis_agent import SentimentAnalysisAgent
from agents.recommendation_agent import RecommendationAgent
from utils.logger import logger


class AgentState(TypedDict):
    """State structure for the agent workflow."""
    stock_symbol: str
    stock_data: Dict[str, Any]
    news_articles: list
    analysis: Dict[str, Any]
    sentiment: Dict[str, Any]
    recommendations: Dict[str, Any]
    errors: list


class AgentOrchestrator:
    """Orchestrates multiple agents using LangGraph for stock analysis workflow."""
    
    def __init__(self):
        """Initialize the agent orchestrator."""
        self.extraction_agent = StockExtractionAgent()
        self.news_agent = NewsAggregationAgent()
        self.analysis_agent = StockAnalysisAgent()
        self.sentiment_agent = SentimentAnalysisAgent()
        self.recommendation_agent = RecommendationAgent()
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
        self.app = self.workflow.compile()
        
        logger.info("Agent orchestrator initialized")
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow.
        
        Returns:
            Configured StateGraph
        """
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("extract_stock", self._extract_stock_node)
        workflow.add_node("aggregate_news", self._aggregate_news_node)
        workflow.add_node("analyze_stock", self._analyze_stock_node)
        workflow.add_node("analyze_sentiment", self._analyze_sentiment_node)
        workflow.add_node("generate_recommendations", self._generate_recommendations_node)
        
        # Define the flow
        workflow.set_entry_point("extract_stock")
        workflow.add_edge("extract_stock", "aggregate_news")
        workflow.add_edge("aggregate_news", "analyze_stock")
        workflow.add_edge("analyze_stock", "analyze_sentiment")
        workflow.add_edge("analyze_sentiment", "generate_recommendations")
        workflow.add_edge("generate_recommendations", END)
        
        return workflow
    
    async def _extract_stock_node(self, state: AgentState) -> AgentState:
        """Extract stock data node."""
        logger.info(f"Extracting stock data for {state['stock_symbol']}")
        result = await self.extraction_agent.execute({
            "stock_symbol": state["stock_symbol"]
        })
        
        if result["status"] == "success":
            state["stock_data"] = result["stock_data"]
        else:
            state["errors"].append(f"Stock extraction error: {result.get('error', 'Unknown error')}")
        
        return state
    
    async def _aggregate_news_node(self, state: AgentState) -> AgentState:
        """Aggregate news node."""
        logger.info(f"Aggregating news for {state['stock_symbol']}")
        result = await self.news_agent.execute({
            "stock_symbol": state["stock_symbol"],
            "stock_data": state.get("stock_data", {})
        })
        
        if result["status"] == "success":
            state["news_articles"] = result["news_articles"]
        else:
            state["errors"].append(f"News aggregation error: {result.get('error', 'Unknown error')}")
            state["news_articles"] = []
        
        return state
    
    async def _analyze_stock_node(self, state: AgentState) -> AgentState:
        """Analyze stock node."""
        logger.info(f"Analyzing stock {state['stock_symbol']}")
        result = await self.analysis_agent.execute({
            "stock_symbol": state["stock_symbol"],
            "stock_data": state.get("stock_data", {}),
            "news_articles": state.get("news_articles", [])
        })
        
        if result["status"] == "success":
            state["analysis"] = result["analysis"]
        else:
            state["errors"].append(f"Stock analysis error: {result.get('error', 'Unknown error')}")
            state["analysis"] = {}
        
        return state
    
    async def _analyze_sentiment_node(self, state: AgentState) -> AgentState:
        """Analyze sentiment node."""
        logger.info(f"Analyzing sentiment for {state['stock_symbol']}")
        result = await self.sentiment_agent.execute({
            "stock_symbol": state["stock_symbol"],
            "news_articles": state.get("news_articles", []),
            "stock_data": state.get("stock_data", {})
        })
        
        if result["status"] == "success":
            state["sentiment"] = result["sentiment"]
        else:
            state["errors"].append(f"Sentiment analysis error: {result.get('error', 'Unknown error')}")
            state["sentiment"] = {}
        
        return state
    
    async def _generate_recommendations_node(self, state: AgentState) -> AgentState:
        """Generate recommendations node."""
        logger.info(f"Generating recommendations for {state['stock_symbol']}")
        result = await self.recommendation_agent.execute({
            "stock_symbol": state["stock_symbol"],
            "stock_data": state.get("stock_data", {}),
            "news_articles": state.get("news_articles", []),
            "analysis": state.get("analysis", {}),
            "sentiment": state.get("sentiment", {})
        })
        
        if result["status"] == "success":
            state["recommendations"] = result["recommendations"]
        else:
            state["errors"].append(f"Recommendation error: {result.get('error', 'Unknown error')}")
            state["recommendations"] = {}
        
        return state
    
    async def run(self, stock_symbol: str) -> Dict[str, Any]:
        """Run the complete agent workflow.
        
        Args:
            stock_symbol: Stock symbol to analyze
            
        Returns:
            Complete analysis results
        """
        logger.info(f"Starting workflow for {stock_symbol}")
        
        initial_state: AgentState = {
            "stock_symbol": stock_symbol.upper(),
            "stock_data": {},
            "news_articles": [],
            "analysis": {},
            "sentiment": {},
            "recommendations": {},
            "errors": []
        }
        
        try:
            # Run the workflow
            final_state = await self.app.ainvoke(initial_state)
            
            logger.info(f"Workflow completed for {stock_symbol}")
            return {
                "stock_symbol": final_state["stock_symbol"],
                "stock_data": final_state.get("stock_data", {}),
                "news_articles": final_state.get("news_articles", []),
                "analysis": final_state.get("analysis", {}),
                "sentiment": final_state.get("sentiment", {}),
                "recommendations": final_state.get("recommendations", {}),
                "errors": final_state.get("errors", [])
            }
        except Exception as e:
            logger.error(f"Error running workflow for {stock_symbol}: {str(e)}")
            return {
                "stock_symbol": stock_symbol,
                "error": str(e),
                "errors": [str(e)]
            }
