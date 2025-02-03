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
        "limit": 10,
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
                    
                    # Add sentiment display with better formatting
                    if article.get("sentiment_scores"):
                        scores = article["sentiment_scores"]
                        
                        # Calculate overall sentiment
                        max_sentiment = max(scores.items(), key=lambda x: x[1])
                        sentiment_color = {
                            "positive": "🟢",
                            "negative": "🔴",
                            "neutral": "🟡"
                        }.get(max_sentiment[0], "⚪")
                        
                        st.markdown(f"### {sentiment_color} Sentiment Analysis")
                        
                        # Create a more compact display for scores
                        st.progress(scores.get("positive", 0), "Positive")
                        st.progress(scores.get("neutral", 0), "Neutral")
                        st.progress(scores.get("negative", 0), "Negative")
                        
                        # Add numerical scores in small text
                        st.caption(f"""
                        Positive: {scores.get('positive', 0):.2f} |
                        Neutral: {scores.get('neutral', 0):.2f} |
                        Negative: {scores.get('negative', 0):.2f}
                        """)
                
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
