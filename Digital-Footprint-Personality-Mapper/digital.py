import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# -----------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------
st.set_page_config(
    page_title="Digital Footprint Personality Mapper",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS for styling (ONLY background changed to black)
st.markdown("""
    <style>
    /* Global background */
    .stApp {
        background: radial-gradient(circle at top left, #1a1a1a, #000000);
        color: #f5f5f5;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Main content area */
    .main {
        background-color: transparent;
    }

    /* Title + subtitle */
    .title-text {
        text-align: center;
        color: #ffffff;
        font-size: 2.5em;
        font-weight: 700;
        background: linear-gradient(90deg, #4e9af1, #e36ce3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3em;
    }

    .subtitle-text {
        text-align: center;
        color: #d0d0d0;
        font-size: 1.1em;
        margin-bottom: 2em;
    }

    /* Card design */
    .card {
        background: rgba(30, 30, 30, 0.9);
        border-radius: 15px;
        padding: 1.5em;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        color: #e0e0e0;
        transition: all 0.3s ease;
    }
    .card:hover {
        box-shadow: 0 6px 25px rgba(255, 255, 255, 0.15);
        transform: translateY(-2px);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #121212;
        color: #e0e0e0;
    }
    .css-1d391kg, .css-1v3fvcr {
        color: #e0e0e0 !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #999999;
        margin-top: 30px;
        font-size: 0.9em;
    }
    a {
        color: #4e9af1;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------
# HEADER
# -----------------------------------------------------------
st.markdown('<div class="title-text">🧠 Digital Footprint Personality Mapper</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Predict your Big Five personality traits from your social media behavior</div>', unsafe_allow_html=True)

# -----------------------------------------------------------
# SIDEBAR INPUTS
# -----------------------------------------------------------
st.sidebar.header("📊 Input Social Media Metrics")

username = st.sidebar.text_input("Username", "yugal71")
platform = st.sidebar.selectbox("Platform", ["Twitter", "Facebook", "Instagram"])

st.sidebar.markdown("---")
st.sidebar.subheader("Behavioral Metrics")

posts_count = st.sidebar.number_input("Total Posts Analyzed", 0, 1000, 245)
avg_likes = st.sidebar.number_input("Average Likes per Post", 0.0, 100.0, 23.5)
comments_count = st.sidebar.number_input("Total Comments", 0, 10000, 1245)
post_frequency = st.sidebar.slider("Posts per Week", 0, 50, 7)
response_time_hours = st.sidebar.slider("Avg Response Time (hours)", 0, 48, 2)

st.sidebar.markdown("---")
st.sidebar.subheader("Content Analysis")

sentiment_positive = st.sidebar.slider("Positive Sentiment %", 0, 100, 65)
sentiment_neutral = st.sidebar.slider("Neutral Sentiment %", 0, 100, 25)
emoji_usage = st.sidebar.slider("Emoji Usage per Post", 0, 20, 5)
hashtag_usage = st.sidebar.slider("Hashtags per Post", 0, 10, 3)

# Engagement Rate
engagement_rate = (
    (avg_likes + (comments_count / posts_count if posts_count > 0 else 0))
    / posts_count * 100 if posts_count > 0 else 0
)

# -----------------------------------------------------------
# SIMULATED MODEL PREDICTION
# -----------------------------------------------------------
def predict_personality(features):
    traits = {
        "Openness": np.clip(features['sentiment_positive'] / 100 + features['emoji_usage'] * 0.08, 0, 1),
        "Conscientiousness": np.clip(features['post_frequency'] / 50 + (1 - features['response_time_hours'] / 48), 0, 1),
        "Extraversion": np.clip(features['engagement_rate'] / 100 + features['hashtag_usage'] * 0.1, 0, 1),
        "Agreeableness": np.clip(features['sentiment_neutral'] / 100 + features['comments_count'] / 10000, 0, 1),
        "Neuroticism": np.clip((100 - features['sentiment_positive']) / 100 + features['response_time_hours'] / 48, 0, 1)
    }
    return traits

features = { 
    'posts_count': posts_count,
    'avg_likes': avg_likes,
    'comments_count': comments_count,
    'post_frequency': post_frequency,
    'response_time_hours': response_time_hours,
    'sentiment_positive': sentiment_positive,
    'sentiment_neutral': sentiment_neutral,
    'emoji_usage': emoji_usage,
    'hashtag_usage': hashtag_usage,
    'engagement_rate': engagement_rate
}

predicted_traits = predict_personality(features)

# -----------------------------------------------------------
# LAYOUT: LEFT (Summary) | RIGHT (Personality)
# -----------------------------------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📋 Profile Summary")
    st.write(f"**Username:** {username}")
    st.write(f"**Platform:** {platform}")
    st.write(f"**Posts Analyzed:** {posts_count}")
    st.write(f"**Engagement Rate:** {engagement_rate:.2f}%")
    st.write(f"**Avg Response Time:** {response_time_hours} hrs")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎯 Predicted Personality Traits")

    # Bar Chart Visualization
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(predicted_traits.keys()),
        y=list(predicted_traits.values()),
        text=[f"{v*100:.1f}%" for v in predicted_traits.values()],
        textposition="auto",
        marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd', '#e377c2']
    ))
    fig.update_layout(
        template="plotly_dark",
        title="Big Five Personality Traits",
        yaxis=dict(title="Score (0 - 1)", range=[0, 1]),
        xaxis=dict(title="Traits"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig, use_container_width=True)

    for trait, score in predicted_traits.items():
        st.write(f"**{trait}** ({score:.2f})")
        st.progress(float(score))
        if trait == "Openness":
            st.caption("Reflects creativity, curiosity, and openness to new experiences.")
        elif trait == "Conscientiousness":
            st.caption("Shows organization, responsibility, and goal-directed behavior.")
        elif trait == "Extraversion":
            st.caption("Indicates sociability, energy, and enthusiasm in social settings.")
        elif trait == "Agreeableness":
            st.caption("Relates to kindness, empathy, and cooperation with others.")
        elif trait == "Neuroticism":
            st.caption("Represents emotional stability and how one handles stress.")
        st.markdown("---")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------
# FOOTER
# -----------------------------------------------------------
st.markdown("""
<div class="footer">
Developed by <b>Yugal Bilawane</b> |
<a href="https://github.com/Yugal0708" target="_blank">GitHub</a> |
<a href="https://www.linkedin.com/in/yugal-bilawane-1b029b32b" target="_blank">LinkedIn</a><br>
© 2025 Yugal Bilawane. All rights reserved.
</div>
""", unsafe_allow_html=True)
