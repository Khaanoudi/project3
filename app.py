import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from sentiment_utils import (
    create_sentiment_card_html,
    filter_articles_by_sentiment
)

# Configure the page
st.set_page_config(
    page_title="Saudi Stock Market News",
    page_icon="📈",
    layout="wide"
)

# API configuration
API_KEY = "bS2jganHVlFYtAly7ttdHYLrTB0s6BmONWmFEApD"
BASE_URL = "https://api.stockdata.org/v1/news/all"

def fetch_news(days_ago=7):
    # Calculate date N days ago
    published_after = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%dT%H:%M")
    
    params = {
        "countries": "sa",
        "filter_entities": "true",
        "limit": 2,  # Reduced to match API limit
        "published_after": published_after,
        "api_token": API_KEY
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def display_sentiment(article):
    """Display sentiment information for an article"""
    if article.get("entities"):
        st.markdown("### 📊 Market Sentiment")
        
        # Create columns for multiple entities
        num_entities = len(article["entities"])
        if num_entities > 0:
            cols = st.columns(min(num_entities, 2))  # Max 2 columns
            
            for idx, entity in enumerate(article["entities"]):
                if "sentiment_score" in entity:
                    col_idx = idx % 2  # Alternate between columns
                    with cols[col_idx]:
                        html = create_sentiment_card_html(
                            entity, 
                            entity["sentiment_score"]
                        )
                        st.markdown(html, unsafe_allow_html=True)

def main():
    st.title("🇸🇦 Saudi Stock Market News")
    
    # Add filters in sidebar
    st.sidebar.title("Filters")
    
    # Date range filter
    days_ago = st.sidebar.slider("News from last N days", 1, 30, 7)
    
    # Sentiment filter
    sentiment_filter = st.sidebar.multiselect(
        "Filter by Sentiment",
        ["Positive", "Neutral", "Negative"],
        default=["Positive", "Neutral", "Negative"]
    )
    
    # Add refresh button with loading state
    if st.button("🔄 Refresh News"):
        with st.spinner("Fetching latest news..."):
            st.experimental_rerun()
    
    # Fetch and display news
    news_data = fetch_news(days_ago)
    
    if news_data and "data" in news_data:
        filtered_articles = filter_articles_by_sentiment(
            news_data["data"], 
            sentiment_filter
        )
        
        # Display total articles found
        st.caption(f"Found {len(filtered_articles)} articles matching your filters")
        
        for article in filtered_articles:
            with st.container():
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    if article.get("image_url"):
                        st.image(article["image_url"], use_container_width=True)
                    display_sentiment(article)
                
                with col2:
                    st.markdown(f"### {article['title']}")
                    st.markdown(f"📅 *{article['published_at'][:10]}*")
                    st.write(article["description"])
                    
                    if article.get("entities"):
                        st.markdown("**Related Companies:**")
                        for entity in article["entities"]:
                            st.markdown(f"- {entity['name']} ({entity['symbol']})")
                    
                    st.markdown(f"[Read full article]({article['url']})")
                
                st.markdown("---")
    else:
        st.warning("No news data available at the moment.")

if __name__ == "__main__":
    main() 
