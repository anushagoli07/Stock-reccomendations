"""Stock recommendation agent for generating actionable investment recommendations."""

import json
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from utils.logger import logger


class RecommendationAgent(BaseAgent):
    """Agent responsible for generating actionable stock investment recommendations."""
    
    def __init__(self):
        """Initialize recommendation agent."""
        super().__init__(
            name="Stock Recommendation Agent",
            description="Generates actionable investment recommendations based on comprehensive analysis"
        )
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate recommendations based on all analysis data.
        
        Args:
            input_data: Dictionary containing all previous agent outputs:
                - stock_symbol
                - stock_data
                - news_articles
                - analysis
                - sentiment
                
        Returns:
            Dictionary with investment recommendations
        """
        stock_symbol = input_data.get("stock_symbol", "").upper()
        stock_data = input_data.get("stock_data", {})
        analysis = input_data.get("analysis", {})
        sentiment = input_data.get("sentiment", {})
        news_articles = input_data.get("news_articles", [])
        
        logger.info(f"Generating recommendations for: {stock_symbol}")
        
        try:
            # Prepare comprehensive context
            context = f"""
Stock Symbol: {stock_symbol}
Current Price: {stock_data.get('price', 'N/A')}

Stock Analysis:
{json.dumps(analysis, indent=2)}

Market Sentiment:
{json.dumps(sentiment, indent=2)}

Recent News Count: {len(news_articles)}
"""
            
            # Use LLM to generate recommendations
            prompt = f"""Based on the comprehensive analysis below, generate actionable investment recommendations for {stock_symbol}:

{context}

Please provide detailed recommendations in JSON format:
{{
    "primary_recommendation": {{
        "action": "STRONG_BUY/BUY/HOLD/SELL/STRONG_SELL",
        "confidence": confidence_score_0_to_1,
        "target_price": target_price_if_available,
        "time_horizon": "short_term/medium_term/long_term",
        "reasoning": "Detailed reasoning for the recommendation",
        "risk_level": "low/medium/high"
    }},
    "alternative_scenarios": [
        {{
            "scenario": "Scenario description",
            "action": "BUY/HOLD/SELL",
            "probability": probability_0_to_1,
            "target_price": target_price,
            "reasoning": "Why this scenario might occur"
        }}
    ],
    "key_factors": [
        "Factor 1 that influences the recommendation",
        "Factor 2",
        "Factor 3"
    ],
    "entry_strategy": {{
        "recommended_entry_price": entry_price,
        "entry_timing": "immediate/wait_for_pullback/wait_for_breakout",
        "position_sizing": "small/medium/large",
        "stop_loss": stop_loss_price_if_applicable
    }},
    "exit_strategy": {{
        "take_profit_targets": [
            {{"price": target_price_1, "percentage": percentage_of_position}},
            {{"price": target_price_2, "percentage": percentage_of_position}}
        ],
        "exit_conditions": [
            "Condition 1",
            "Condition 2"
        ]
    }},
    "portfolio_considerations": {{
        "sector_allocation": "Consider current sector exposure",
        "diversification": "Diversification impact",
        "correlation": "Correlation with existing holdings"
    }}
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
                
                recommendations = json.loads(response_text)
            except json.JSONDecodeError:
                logger.warning(f"Could not parse JSON from LLM response, using fallback")
                recommendations = {
                    "primary_recommendation": {
                        "action": "HOLD",
                        "confidence": 0.5,
                        "target_price": None,
                        "time_horizon": "medium_term",
                        "reasoning": "Based on available data, maintaining current position is recommended",
                        "risk_level": "medium"
                    },
                    "alternative_scenarios": [],
                    "key_factors": [],
                    "entry_strategy": {
                        "recommended_entry_price": stock_data.get("price"),
                        "entry_timing": "wait",
                        "position_sizing": "medium",
                        "stop_loss": None
                    },
                    "exit_strategy": {
                        "take_profit_targets": [],
                        "exit_conditions": []
                    },
                    "portfolio_considerations": {
                        "sector_allocation": "N/A",
                        "diversification": "N/A",
                        "correlation": "N/A"
                    }
                }
            
            logger.info(f"Successfully generated recommendations for {stock_symbol}")
            return {
                "status": "success",
                "recommendations": recommendations
            }
            
        except Exception as e:
            logger.error(f"Error generating recommendations for {stock_symbol}: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "recommendations": {
                    "primary_recommendation": {
                        "action": "HOLD",
                        "confidence": 0.0,
                        "reasoning": f"Error generating recommendation: {str(e)}"
                    }
                }
            }
