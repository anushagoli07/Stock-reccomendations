"""Stock analysis agent for analyzing stock performance and trends."""

import json
from typing import Dict, Any
from agents.base_agent import BaseAgent
from utils.logger import logger


class StockAnalysisAgent(BaseAgent):
    """Agent responsible for analyzing stock performance, trends, and metrics."""
    
    def __init__(self):
        """Initialize stock analysis agent."""
        super().__init__(
            name="Stock Analysis Agent",
            description="Analyzes stock performance, trends, technical indicators, and financial metrics"
        )
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze stock data and generate insights.
        
        Args:
            input_data: Dictionary containing 'stock_symbol', 'stock_data', and 'news_articles'
            
        Returns:
            Dictionary with analysis results
        """
        stock_symbol = input_data.get("stock_symbol", "").upper()
        stock_data = input_data.get("stock_data", {})
        news_articles = input_data.get("news_articles", [])
        
        logger.info(f"Analyzing stock: {stock_symbol}")
        
        try:
            # Prepare context for analysis
            context = f"""
Stock Data:
{json.dumps(stock_data, indent=2)}

Recent News Summary:
{json.dumps(news_articles[:5], indent=2) if news_articles else "No recent news available"}
"""
            
            # Use LLM to perform comprehensive analysis
            prompt = f"""Perform a comprehensive analysis of {stock_symbol} stock based on the following data:

{context}

Please provide a detailed analysis in JSON format with the following structure:
{{
    "technical_analysis": {{
        "trend": "bullish/bearish/neutral",
        "support_level": support_price,
        "resistance_level": resistance_price,
        "momentum": "strong/weak/neutral",
        "volatility": "high/medium/low"
    }},
    "fundamental_analysis": {{
        "valuation": "overvalued/undervalued/fair",
        "financial_health": "strong/moderate/weak",
        "growth_prospects": "excellent/good/moderate/poor",
        "competitive_position": "strong/moderate/weak"
    }},
    "risk_assessment": {{
        "overall_risk": "low/medium/high",
        "market_risk": "low/medium/high",
        "company_specific_risk": "low/medium/high",
        "risk_factors": ["risk factor 1", "risk factor 2"]
    }},
    "key_insights": [
        "Insight 1",
        "Insight 2",
        "Insight 3"
    ],
    "strengths": [
        "Strength 1",
        "Strength 2"
    ],
    "weaknesses": [
        "Weakness 1",
        "Weakness 2"
    ],
    "opportunities": [
        "Opportunity 1",
        "Opportunity 2"
    ],
    "threats": [
        "Threat 1",
        "Threat 2"
    ]
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
                
                analysis = json.loads(response_text)
            except json.JSONDecodeError:
                logger.warning(f"Could not parse JSON from LLM response, using fallback")
                analysis = {
                    "technical_analysis": {
                        "trend": "neutral",
                        "support_level": None,
                        "resistance_level": None,
                        "momentum": "neutral",
                        "volatility": "medium"
                    },
                    "fundamental_analysis": {
                        "valuation": "fair",
                        "financial_health": "moderate",
                        "growth_prospects": "moderate",
                        "competitive_position": "moderate"
                    },
                    "risk_assessment": {
                        "overall_risk": "medium",
                        "market_risk": "medium",
                        "company_specific_risk": "medium",
                        "risk_factors": []
                    },
                    "key_insights": [],
                    "strengths": [],
                    "weaknesses": [],
                    "opportunities": [],
                    "threats": []
                }
            
            logger.info(f"Successfully analyzed {stock_symbol}")
            return {
                "status": "success",
                "analysis": analysis
            }
            
        except Exception as e:
            logger.error(f"Error analyzing {stock_symbol}: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "analysis": {}
            }
