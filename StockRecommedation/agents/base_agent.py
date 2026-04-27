"""Base agent class for all stock analysis agents."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from config.settings import settings
from utils.logger import logger


class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    def __init__(self, name: str, description: str):
        """Initialize base agent.
        
        Args:
            name: Agent name
            description: Agent description
        """
        self.name = name
        self.description = description
        self.llm = ChatGoogleGenerativeAI(
            model=settings.model_name,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            google_api_key=settings.gemini_api_key
        )
        self.tools = self._initialize_tools()
        logger.info(f"Initialized agent: {self.name}")
    
    def _initialize_tools(self) -> List[Tool]:
        """Initialize tools available to the agent.
        
        Returns:
            List of LangChain tools
        """
        tools = []
        
        # Web search tool (Google Serper API - requires SERPER_API_KEY)
        try:
            search = GoogleSerperAPIWrapper(serper_api_key=settings.serper_api_key)
            search_tool = Tool(
                name="google_search",
                description="Search Google for current information about stocks, news, and market trends",
                func=search.run
            )
            tools.append(search_tool)
            logger.info("Initialized Google Serper API search tool")
        except Exception as e:
            logger.warning(f"Could not initialize Google Serper API search tool: {e}")
            # Fallback to a simple web search tool
            tools.append(self._create_web_search_tool())
        
        return tools
    
    def _create_web_search_tool(self) -> Tool:
        """Create a basic web search tool as fallback.
        
        Returns:
            LangChain Tool for web search
        """
        def web_search(query: str) -> str:
            """Search the web for information."""
            logger.warning("Using placeholder web search. Configure SERPER_API_KEY for better results.")
            return f"Search results for: {query}"
        
        return Tool(
            name="web_search",
            description="Search the web for current information about stocks, news, and market trends",
            func=web_search
        )
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main task.
        
        Args:
            input_data: Input data dictionary
            
        Returns:
            Output data dictionary
        """
        pass
    
    def get_name(self) -> str:
        """Get agent name."""
        return self.name
    
    def get_description(self) -> str:
        """Get agent description."""
        return self.description
