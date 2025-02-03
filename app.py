import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# Configure the page
st.set_page_config(
    page_title="Saudi Stock Market News",
    page_icon="📈",
    layout="wide"
)

# API configuration
API_KEY = "bS2jganHVlFYtAly7ttdHYLrTB0s6BmONWmFEApD"
BASE_URL = "https://api.stockdata.org/v1/news/all"

def fetch_news():
    # Calculate date 7 days ago
    published_after = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M")
    
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
    """Helper function to display sentiment information"""
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
                        score = entity["sentiment_score"]
                        
                        # Determine sentiment category and color
                        if score > 0.6:
                            color = "#28a745"  # Green
                            emoji = "🟢"
                            category = "Positive"
                        elif score < 0.4:
                            color = "#dc3545"  # Red
                            emoji = "🔴"
                            category = "Negative"
                        else:
                            color = "#ffc107"  # Yellow
                            emoji = "🟡"
                            category = "Neutral"
                        
                        # Company name with symbol
                        st.markdown(f"""
                        <div style='padding: 10px; border-radius: 5px; background-color: rgba(0,0,0,0.05)'>
                            <h4>{emoji} {entity['name']}</h4>
                            <p style='color: gray; font-size: 0.8em;'>{entity['symbol']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Progress bar with custom color
                        st.markdown(f"""
                        <div style='margin-bottom: 5px;'>
                            <div style='
                                width: {score * 100}%;
                                height: 10px;
                                background-color: {color};
                                border-radius: 5px;
                            '></div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Score and category
                        st.markdown(f"""
                        <p style='text-align: right; color: {color}; font-weight: bold;'>
                            {score:.2f} | {category}
                        </p>
                        """, unsafe_allow_html=True)

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
    news_data = fetch_news()
    
    if news_data and "data" in news_data:
        # Display total articles found
        st.caption(f"Found {len(news_data['data'])} articles")
        
        for article in news_data["data"]:
            with st.container():
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    if article.get("image_url"):
                        st.image(article["image_url"], use_container_width=True)
                    display_sentiment(article)
                
                with col2:
                    st.subheader(article["title"])
                    st.write(f"📅 Published: {article['published_at'][:10]}")
                    st.write(article["description"])
                    
                    if article.get("entities"):
                        st.write("**Related Companies:**")
                        for entity in article["entities"]:
                            st.write(f"- {entity['name']} ({entity['symbol']})")
                    
                    st.markdown(f"[Read more]({article['url']})")
                
                st.markdown("---")
    else:
        st.warning("No news data available at the moment.")

if __name__ == "__main__":
    main() 
