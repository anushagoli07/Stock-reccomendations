"""Stock extraction agent for gathering real-time stock data."""

import json
from typing import Dict, Any
from agents.base_agent import BaseAgent
from utils.logger import logger


class StockExtractionAgent(BaseAgent):
    """Agent responsible for extracting real-time stock data from web sources."""
    
    def __init__(self):
        """Initialize stock extraction agent."""
        super().__init__(
            name="Stock Extraction Agent",
            description="Extracts real-time stock data, prices, and basic information from web sources"
        )
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract stock data for the given symbol.
        
        Args:
            input_data: Dictionary containing 'stock_symbol'
            
        Returns:
            Dictionary with extracted stock data
        """
        stock_symbol = input_data.get("stock_symbol", "").upper()
        logger.info(f"Extracting stock data for: {stock_symbol}")
        
        try:
            # Use LLM with tools to extract stock information
            search_query = f"{stock_symbol} stock price current market data financial information"
            
            # Search for stock information
            if self.tools:
                search_results = self.tools[0].run(search_query)
                logger.info(f"Search results obtained for {stock_symbol}")
            else:
                search_results = f"Information about {stock_symbol} stock"
            
            # Use LLM to extract structured data from search results
            prompt = f"""Extract the following information about {stock_symbol} stock from the search results:

Search Results:
{search_results}

Please extract and return a JSON object with the following structure:
{{
    "symbol": "{stock_symbol}",
    "name": "Company name",
    "price": current_price,
    "change": price_change,
    "change_percent": percentage_change,
    "volume": trading_volume,
    "market_cap": market_capitalization,
    "pe_ratio": price_to_earnings_ratio,
    "dividend_yield": dividend_yield,
    "52_week_high": 52_week_high_price,
    "52_week_low": 52_week_low_price,
    "sector": industry_sector,
    "industry": industry_name
}}

If any information is not available, use null for that field. Return only valid JSON."""

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
                
                stock_data = json.loads(response_text)
            except json.JSONDecodeError:
                # Fallback: create basic structure
                logger.warning(f"Could not parse JSON from LLM response, using fallback")
                stock_data = {
                    "symbol": stock_symbol,
                    "name": f"{stock_symbol} Corporation",
                    "price": None,
                    "change": None,
                    "change_percent": None,
                    "volume": None,
                    "market_cap": None,
                    "pe_ratio": None,
                    "dividend_yield": None,
                    "52_week_high": None,
                    "52_week_low": None,
                    "sector": None,
                    "industry": None
                }
            
            logger.info(f"Successfully extracted data for {stock_symbol}")
            return {
                "status": "success",
                "stock_data": stock_data,
                "raw_search_results": search_results
            }
            
        except Exception as e:
            logger.error(f"Error extracting stock data for {stock_symbol}: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "stock_data": {
                    "symbol": stock_symbol,
                    "name": None,
                    "price": None
                }
            }
