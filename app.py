# app.py

import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from services.notification_service import NotificationService
from core.data.api_client import CricbuzzAPIClient
from core.analytics.player_analyzer import PlayerAnalyzer
import time

# Initialize the NotificationService instance
notification_service = NotificationService()

# Initialize external API client and other services
api_client = CricbuzzAPIClient(api_key="fd207dab-6b6c-40dc-8782-de1b1b173371")

# Main Streamlit UI
st.title("Fantasy Cricket Assistant")
st.sidebar.title("User Options")

# Subscription Section
if 'user_id' not in st.session_state:
    st.session_state.user_id = "user" + str(time.time()).split(".")[0]  # Generate a unique user ID for session

user_id = st.session_state.user_id

st.sidebar.subheader(f"User ID: {user_id}")
subscription_button = st.sidebar.button("Subscribe for Live Notifications")

if subscription_button:
    notification_service.subscribe(user_id)
    st.sidebar.success(f"Subscribed to live notifications for {user_id}!")

unsubscribe_button = st.sidebar.button("Unsubscribe")

if unsubscribe_button:
    notification_service.unsubscribe(user_id)
    st.sidebar.warning(f"Unsubscribed from live notifications for {user_id}.")

# Live Match Update Section
st.subheader("Live Match Updates")

def show_live_match_updates():
    """Fetch live match status and notify subscribers."""
    live_match = api_client.get_live_match_status()

    # Debug: Print the response to understand its structure
    st.write("API Response:", live_match)

    # Check if the response contains the required data
    if "error" in live_match:
        st.error(live_match["error"])
    else:
        # Adjust based on the actual response structure
        match_info = live_match.get("matches", [{}])[0]  # Example: Adjust this key
        team1 = match_info.get("team-1", "Unknown Team")
        team2 = match_info.get("team-2", "Unknown Team")
        status = match_info.get("status", "No status available")

        st.write(f"Match: {team1} vs {team2}")
        st.write(f"Status: {status}")

        # Trigger notifications for subscribers
        notification_service.send_notification(user_id, f"Live match update: {status}")

# Add a button to fetch and show live match updates
if st.button("Fetch Live Updates"):
    show_live_match_updates()

# Example: Analytics and Fantasy Insights
st.subheader("Player Analytics")
player_id = st.selectbox("Select Player", ["Player 1", "Player 2", "Player 3"])  # Simulate player selection

# Fetch and display player analysis
player_analysis = PlayerAnalyzer.analyze_player(player_id)
st.write(f"Player Analysis for {player_id}: {player_analysis}")

