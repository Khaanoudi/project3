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
        st.markdown("### 📊 Sentiment Analysis")
        
        for entity in article["entities"]:
            if "sentiment_score" in entity:
                score = entity["sentiment_score"]
                
                # Determine sentiment category based on score
                if score > 0.6:
                    emoji = "🟢"
                    category = "Positive"
                elif score < 0.4:
                    emoji = "🔴"
                    category = "Negative"
                else:
                    emoji = "🟡"
                    category = "Neutral"
                
                st.markdown(f"**{emoji} {entity['name']}**")
                st.progress(score, "Sentiment Score")
                st.caption(f"Score: {score:.2f} ({category})")
                st.markdown("---")

def main():
    st.title("🇸🇦 Saudi Stock Market News")
    
    # Add refresh button
    if st.button("🔄 Refresh News"):
        st.experimental_rerun()
    
    news_data = fetch_news()
    
    if news_data and "data" in news_data:
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
