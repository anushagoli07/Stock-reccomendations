"""Streamlit frontend application for Stock Recommendation System."""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, Any, Optional
import time

# Page configuration
st.set_page_config(
    page_title="Stock Recommendation AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .recommendation-box {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .buy {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
    }
    .sell {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
    }
    .hold {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
    }
    </style>
""", unsafe_allow_html=True)

# Backend API URL
API_URL = "http://localhost:8000"


def check_api_health() -> bool:
    """Check if the backend API is running."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def analyze_stock(stock_symbol: str) -> Optional[Dict[str, Any]]:
    """Call the backend API to analyze a stock.
    
    Args:
        stock_symbol: Stock symbol to analyze
        
    Returns:
        Analysis results or None if error
    """
    try:
        response = requests.post(
            f"{API_URL}/api/v1/analyze",
            json={"stock_symbol": stock_symbol},
            timeout=300  # 5 minutes timeout for analysis
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None


def display_stock_data(data: Dict[str, Any]):
    """Display stock data in a nice format."""
    stock_data = data.get("stock_data", {})
    
    if not stock_data:
        st.warning("Stock data not available")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Price",
            f"${stock_data.get('price', 'N/A')}" if stock_data.get('price') else "N/A"
        )
    
    with col2:
        change = stock_data.get('change_percent', 0)
        st.metric(
            "Change %",
            f"{change:.2f}%" if change else "N/A",
            delta=f"{change:.2f}%" if change else None
        )
    
    with col3:
        st.metric(
            "Volume",
            f"{stock_data.get('volume', 0):,}" if stock_data.get('volume') else "N/A"
        )
    
    with col4:
        market_cap = stock_data.get('market_cap')
        if market_cap:
            # If market_cap is a string (e.g., "3.97T"), display as-is with $ prefix if not already present
            market_cap_str = str(market_cap)
            if not market_cap_str.startswith('$'):
                market_cap_display = f"${market_cap_str}"
            else:
                market_cap_display = market_cap_str
        else:
            market_cap_display = "N/A"
        st.metric("Market Cap", market_cap_display)
    
    # Additional metrics
    if stock_data.get('pe_ratio') or stock_data.get('dividend_yield'):
        col5, col6 = st.columns(2)
        with col5:
            st.metric("P/E Ratio", f"{stock_data.get('pe_ratio', 'N/A')}" if stock_data.get('pe_ratio') else "N/A")
        with col6:
            st.metric("Dividend Yield", f"{stock_data.get('dividend_yield', 'N/A')}%" if stock_data.get('dividend_yield') else "N/A")


def display_sentiment(sentiment: Dict[str, Any]):
    """Display sentiment analysis."""
    if not sentiment:
        return
    
    st.subheader("📊 Market Sentiment")
    
    overall = sentiment.get("overall_sentiment", "neutral")
    score = sentiment.get("sentiment_score", 0.0)
    
    # Sentiment gauge
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Sentiment Score"},
        delta = {'reference': 0},
        gauge = {
            'axis': {'range': [-100, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [-100, -50], 'color': "lightgray"},
                {'range': [-50, 0], 'color': "gray"},
                {'range': [0, 50], 'color': "lightgreen"},
                {'range': [50, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=250)
    st.plotly_chart(fig, use_container_width=True)
    
    # Sentiment details
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Overall Sentiment:** {overall.replace('_', ' ').title()}")
    with col2:
        st.write(f"**Sentiment Trend:** {sentiment.get('sentiment_trend', 'N/A').title()}")
    with col3:
        st.write(f"**Confidence:** {sentiment.get('confidence_level', 0.0):.1%}")


def display_recommendations(recommendations: Dict[str, Any]):
    """Display stock recommendations."""
    if not recommendations:
        return
    
    st.subheader("💡 Investment Recommendations")
    
    primary = recommendations.get("primary_recommendation", {})
    if primary:
        action = primary.get("action", "HOLD")
        confidence = primary.get("confidence", 0.0)
        reasoning = primary.get("reasoning", "")
        target_price = primary.get("target_price")
        time_horizon = primary.get("time_horizon", "N/A")
        
        # Determine CSS class based on action
        css_class = "hold"
        if "BUY" in action.upper():
            css_class = "buy"
        elif "SELL" in action.upper():
            css_class = "sell"
        
        st.markdown(f"""
        <div class="recommendation-box {css_class}">
            <h3>Primary Recommendation: {action.replace('_', ' ').title()}</h3>
            <p><strong>Confidence:</strong> {confidence:.1%}</p>
            <p><strong>Time Horizon:</strong> {time_horizon.replace('_', ' ').title()}</p>
            {f'<p><strong>Target Price:</strong> ${target_price:.2f}</p>' if target_price else ''}
            <p><strong>Reasoning:</strong> {reasoning}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Key factors
    key_factors = recommendations.get("key_factors", [])
    if key_factors:
        st.write("**Key Factors:**")
        for factor in key_factors:
            st.write(f"- {factor}")


def display_analysis(analysis: Dict[str, Any]):
    """Display stock analysis."""
    if not analysis:
        return
    
    st.subheader("🔍 Detailed Analysis")
    
    # Technical Analysis
    technical = analysis.get("technical_analysis", {})
    if technical:
        st.write("**Technical Analysis:**")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"- Trend: {technical.get('trend', 'N/A').title()}")
            st.write(f"- Momentum: {technical.get('momentum', 'N/A').title()}")
        with col2:
            st.write(f"- Volatility: {technical.get('volatility', 'N/A').title()}")
            if technical.get('support_level'):
                st.write(f"- Support: ${technical.get('support_level'):.2f}")
            if technical.get('resistance_level'):
                st.write(f"- Resistance: ${technical.get('resistance_level'):.2f}")
    
    # SWOT Analysis
    col1, col2 = st.columns(2)
    with col1:
        strengths = analysis.get("strengths", [])
        if strengths:
            st.write("**Strengths:**")
            for s in strengths:
                st.write(f"✅ {s}")
        
        weaknesses = analysis.get("weaknesses", [])
        if weaknesses:
            st.write("**Weaknesses:**")
            for w in weaknesses:
                st.write(f"❌ {w}")
    
    with col2:
        opportunities = analysis.get("opportunities", [])
        if opportunities:
            st.write("**Opportunities:**")
            for o in opportunities:
                st.write(f"🚀 {o}")
        
        threats = analysis.get("threats", [])
        if threats:
            st.write("**Threats:**")
            for t in threats:
                st.write(f"⚠️ {t}")


def display_news(news_articles: list):
    """Display news articles."""
    if not news_articles:
        return
    
    st.subheader("📰 Recent News")
    
    for i, article in enumerate(news_articles[:5], 1):
        with st.expander(f"{i}. {article.get('title', 'No title')}"):
            st.write(f"**Source:** {article.get('source', 'Unknown')}")
            if article.get('published_date'):
                st.write(f"**Date:** {article.get('published_date')}")
            if article.get('summary'):
                st.write(f"**Summary:** {article.get('summary')}")
            if article.get('url'):
                st.write(f"**Link:** {article.get('url')}")
            if article.get('sentiment'):
                st.write(f"**Sentiment:** {article.get('sentiment').title()}")


def main():
    """Main application function."""
    # Header
    st.markdown('<div class="main-header">📈 Stock Recommendation AI</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Health Check
        api_status = check_api_health()
        if api_status:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Not Available")
            st.info("Please start the FastAPI backend server first.")
            st.code("cd backend\nuvicorn main:app --reload --port 8000")
        
        st.markdown("---")
        st.markdown("### About")
        st.info("""
        This application uses agentic AI to:
        - Extract real-time stock data
        - Aggregate relevant news
        - Analyze stock performance
        - Analyze market sentiment
        - Generate investment recommendations
        """)
    
    # Main content
    if not api_status:
        st.warning("⚠️ Please start the backend API server to use this application.")
        return
    
    # Stock input
    col1, col2 = st.columns([3, 1])
    with col1:
        stock_symbol = st.text_input(
            "Enter Stock Symbol",
            placeholder="e.g., AAPL, MSFT, GOOGL",
            value=""
        ).upper()
    
    with col2:
        st.write("")  # Spacing
        analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
    
    if analyze_button and stock_symbol:
        with st.spinner(f"Analyzing {stock_symbol}... This may take a few minutes."):
            result = analyze_stock(stock_symbol)
        
        if result:
            # Display results
            st.success(f"Analysis complete for {stock_symbol}!")
            
            # Stock Data
            st.header("📊 Stock Information")
            display_stock_data(result)
            
            st.markdown("---")
            
            # Recommendations (most important, show first)
            display_recommendations(result.get("recommendations", {}))
            
            st.markdown("---")
            
            # Sentiment
            display_sentiment(result.get("sentiment", {}))
            
            st.markdown("---")
            
            # Analysis
            display_analysis(result.get("analysis", {}))
            
            st.markdown("---")
            
            # News
            display_news(result.get("news_articles", []))
            
            # Errors (if any)
            errors = result.get("errors", [])
            if errors:
                st.error("⚠️ Some errors occurred during analysis:")
                for error in errors:
                    st.write(f"- {error}")
        else:
            st.error("Failed to analyze stock. Please check the backend logs.")
    
    elif analyze_button and not stock_symbol:
        st.warning("Please enter a stock symbol.")


if __name__ == "__main__":
    main()
