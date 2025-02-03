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
                        st.image(article["image_url"], use_column_width=True)
                    
                    # Add sentiment display
                    if article.get("sentiment"):
                        sentiment = article["sentiment"]
                        sentiment_color = {
                            "positive": "🟢 Positive",
                            "negative": "🔴 Negative",
                            "neutral": "🟡 Neutral"
                        }.get(sentiment.lower(), "⚪ Unknown")
                        
                        st.markdown(f"**Sentiment:** {sentiment_color}")
                        
                        # Display sentiment scores if available
                        if isinstance(article.get("sentiment_scores"), dict):
                            scores = article["sentiment_scores"]
                            st.markdown("**Sentiment Scores:**")
                            col1_score, col2_score, col3_score = st.columns(3)
                            with col1_score:
                                st.metric("Positive", f"{scores.get('positive', 0):.2f}")
                            with col2_score:
                                st.metric("Neutral", f"{scores.get('neutral', 0):.2f}")
                            with col3_score:
                                st.metric("Negative", f"{scores.get('negative', 0):.2f}")
                
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
