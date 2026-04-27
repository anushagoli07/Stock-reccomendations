"""Sentiment analysis agent for analyzing market sentiment."""

import json
from typing import Dict, Any
from agents.base_agent import BaseAgent
from utils.logger import logger


class SentimentAnalysisAgent(BaseAgent):
    """Agent responsible for analyzing market sentiment from news and social media."""
    
    def __init__(self):
        """Initialize sentiment analysis agent."""
        super().__init__(
            name="Sentiment Analysis Agent",
            description="Analyzes market sentiment from news articles, social media, and market indicators"
        )
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze sentiment for the given stock.
        
        Args:
            input_data: Dictionary containing 'stock_symbol', 'news_articles', and 'stock_data'
            
        Returns:
            Dictionary with sentiment analysis results
        """
        stock_symbol = input_data.get("stock_symbol", "").upper()
        news_articles = input_data.get("news_articles", [])
        stock_data = input_data.get("stock_data", {})
        
        logger.info(f"Analyzing sentiment for: {stock_symbol}")
        
        try:
            # Prepare context
            context = f"""
Stock Symbol: {stock_symbol}
Current Price: {stock_data.get('price', 'N/A')}
Price Change: {stock_data.get('change_percent', 'N/A')}%

Recent News Articles:
{json.dumps(news_articles[:10], indent=2) if news_articles else "No news articles available"}
"""
            
            # Use LLM to analyze sentiment
            prompt = f"""Analyze the overall market sentiment for {stock_symbol} based on the following information:

{context}

Please provide a comprehensive sentiment analysis in JSON format:
{{
    "overall_sentiment": "very_positive/positive/neutral/negative/very_negative",
    "sentiment_score": sentiment_score_from_negative_1_to_1,
    "news_sentiment": {{
        "positive_count": number_of_positive_articles,
        "negative_count": number_of_negative_articles,
        "neutral_count": number_of_neutral_articles,
        "average_sentiment": average_sentiment_score
    }},
    "market_sentiment": {{
        "investor_sentiment": "bullish/bearish/neutral",
        "analyst_sentiment": "positive/negative/neutral",
        "retail_sentiment": "positive/negative/neutral"
    }},
    "key_sentiment_drivers": [
        "Driver 1",
        "Driver 2",
        "Driver 3"
    ],
    "sentiment_trend": "improving/declining/stable",
    "confidence_level": confidence_score_0_to_1
}}

Return only valid JSON."""

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
                
                sentiment = json.loads(response_text)
            except json.JSONDecodeError:
                logger.warning(f"Could not parse JSON from LLM response, using fallback")
                sentiment = {
                    "overall_sentiment": "neutral",
                    "sentiment_score": 0.0,
                    "news_sentiment": {
                        "positive_count": 0,
                        "negative_count": 0,
                        "neutral_count": len(news_articles),
                        "average_sentiment": 0.0
                    },
                    "market_sentiment": {
                        "investor_sentiment": "neutral",
                        "analyst_sentiment": "neutral",
                        "retail_sentiment": "neutral"
                    },
                    "key_sentiment_drivers": [],
                    "sentiment_trend": "stable",
                    "confidence_level": 0.5
                }
            
            logger.info(f"Successfully analyzed sentiment for {stock_symbol}")
            return {
                "status": "success",
                "sentiment": sentiment
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment for {stock_symbol}: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "sentiment": {
                    "overall_sentiment": "neutral",
                    "sentiment_score": 0.0
                }
            }
