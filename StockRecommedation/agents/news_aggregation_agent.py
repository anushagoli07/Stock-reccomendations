"""News aggregation agent for collecting relevant stock market news."""

import json
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from utils.logger import logger


class NewsAggregationAgent(BaseAgent):
    """Agent responsible for aggregating relevant stock market news."""
    
    def __init__(self):
        """Initialize news aggregation agent."""
        super().__init__(
            name="News Aggregation Agent",
            description="Collects and filters relevant stock market news from various sources"
        )
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregate news for the given stock symbol.
        
        Args:
            input_data: Dictionary containing 'stock_symbol' and optionally 'stock_data'
            
        Returns:
            Dictionary with aggregated news articles
        """
        stock_symbol = input_data.get("stock_symbol", "").upper()
        logger.info(f"Aggregating news for: {stock_symbol}")
        
        try:
            # Search for recent news
            search_query = f"{stock_symbol} stock news recent updates market trends financial news"
            
            if self.tools:
                search_results = self.tools[0].run(search_query)
                logger.info(f"News search results obtained for {stock_symbol}")
            else:
                search_results = f"Recent news about {stock_symbol}"
            
            # Use LLM to extract and structure news articles
            prompt = f"""From the following search results about {stock_symbol}, extract and structure the most relevant news articles:

Search Results:
{search_results}

Please return a JSON array of news articles with the following structure:
[
    {{
        "title": "Article title",
        "source": "News source",
        "url": "Article URL if available",
        "published_date": "Publication date",
        "summary": "Brief summary of the article",
        "relevance_score": relevance_score_0_to_1,
        "sentiment": "positive/negative/neutral"
    }}
]

Return at least 5-10 most relevant articles. Return only valid JSON array."""

            response = await self.llm.ainvoke(prompt)
            response_text = response.content
            
            # Parse JSON from response
            try:
                # Extract JSON from markdown code blocks if present
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    response_text = response_text[json_start:json_end].strip()
                elif "```" in response_text:
                    json_start = response_text.find("```") + 3
                    json_end = response_text.find("```", json_start)
                    response_text = response_text[json_start:json_end].strip()
                
                news_articles = json.loads(response_text)
                if not isinstance(news_articles, list):
                    news_articles = [news_articles]
            except json.JSONDecodeError:
                logger.warning(f"Could not parse JSON from LLM response, using fallback")
                news_articles = [
                    {
                        "title": f"News about {stock_symbol}",
                        "source": "Various sources",
                        "url": None,
                        "published_date": "Recent",
                        "summary": "Recent market news and updates",
                        "relevance_score": 0.5,
                        "sentiment": "neutral"
                    }
                ]
            
            # Sort by relevance
            news_articles.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
            
            logger.info(f"Successfully aggregated {len(news_articles)} news articles for {stock_symbol}")
            return {
                "status": "success",
                "news_articles": news_articles[:10],  # Top 10 most relevant
                "total_articles": len(news_articles)
            }
            
        except Exception as e:
            logger.error(f"Error aggregating news for {stock_symbol}: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "news_articles": []
            }
