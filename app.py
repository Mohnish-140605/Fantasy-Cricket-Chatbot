# app.py

import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from services.notification_service import NotificationService
from core.data.api_client import CricbuzzAPIClient
from core.analytics.player_analyzer import PlayerAnalyzer
import time
# from cricbuzz import Cricbuzz   # <-- Remove or comment out this line
import requests
import os
from dotenv import load_dotenv

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

# Add match type filter in the sidebar
match_types = ["All", "t20", "odi", "test"]
selected_match_type = st.sidebar.selectbox("Filter by Match Type", match_types, index=0)

# Add custom CSS for match cards and badges
st.markdown("""
    <style>
    .match-card {
        background: #23272f;
        border-radius: 18px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.25);
        padding: 28px 24px 18px 24px;
        margin-bottom: 32px;
        transition: box-shadow 0.2s, transform 0.2s;
        border: 2px solid #1f77b4;
        position: relative;
    }
    .match-card:hover {
        box-shadow: 0 16px 40px rgba(31,119,180,0.25);
        border-color: #ff7f0e;
        transform: scale(1.02);
    }
    .match-badge {
        display: inline-block;
        padding: 2px 12px;
        border-radius: 12px;
        font-size: 0.95em;
        font-weight: bold;
        margin-bottom: 8px;
        background: linear-gradient(90deg,#1f77b4,#2ca02c);
        color: #fff;
        margin-right: 8px;
        box-shadow: 0 2px 8px rgba(31,119,180,0.15);
    }
    .match-status-live {
        background: #e63946;
        color: #fff;
        animation: pulse 1.2s infinite;
    }
    .match-status-ended {
        background: #888;
        color: #fff;
    }
    .match-status-abandoned {
        background: #ffb703;
        color: #23272f;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 #e6394666; }
        70% { box-shadow: 0 0 0 10px #e6394600; }
        100% { box-shadow: 0 0 0 0 #e6394600; }
    }
    .match-teams {
        font-size: 1.4em;
        font-weight: bold;
        margin-bottom: 6px;
    }
    .match-venue {
        color: #bbb;
        font-size: 1em;
        margin-bottom: 10px;
    }
    .match-score {
        color: #ff7f0e;
        font-size: 1.1em;
        margin-bottom: 2px;
    }
    .match-logo {
        border-radius: 10px;
        border: 2px solid #444;
        background: #fff;
        margin-bottom: 6px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
    }
    .winner {
        color: #2ca02c;
        font-weight: bold;
        font-size: 1.1em;
        text-shadow: 0 2px 8px #2ca02c33;
    }
    </style>
""", unsafe_allow_html=True)

def get_match_type_icon(match_type):
    if match_type.lower() == "t20":
        return "🏏"
    elif match_type.lower() == "odi":
        return "⚡"
    elif match_type.lower() == "test":
        return "🛡️"
    else:
        return "🏟️"

def get_status_class(status):
    if "live" in status.lower():
        return "match-status-live"
    elif "abandon" in status.lower() or "no result" in status.lower():
        return "match-status-abandoned"
    elif "won" in status.lower() or "ended" in status.lower() or "draw" in status.lower():
        return "match-status-ended"
    else:
        return "match-status-live"

def highlight_winner(team, status):
    if team.lower() in status.lower():
        return f'<span class="winner">{team}</span>'
    return team

# Load environment variables from .env file
load_dotenv()

def get_live_scores(match_type_filter="All"):
    api_key = os.getenv("CRICAPI_KEY")
    url = f"https://api.cricapi.com/v1/currentMatches?apikey={api_key}&offset=0"
    response = requests.get(url)
    data = response.json()
    live_matches = []
    if data.get("status") == "success":
        for match in data.get("data", []):
            if match.get("matchStarted"):
                if match_type_filter != "All" and match.get("matchType", "").lower() != match_type_filter.lower():
                    continue
                team1 = match.get("teams", ["Team 1", "Team 2"])[0]
                team2 = match.get("teams", ["Team 1", "Team 2"])[1]
                team1_logo = match.get("teamInfo", [{}])[0].get("img", "")
                team2_logo = match.get("teamInfo", [{}])[1].get("img", "")
                status = match.get("status", "No status")
                venue = match.get("venue", "Unknown Venue")
                match_type = match.get("matchType", "Unknown")
                scores = []
                if "score" in match and match["score"]:
                    for inning in match["score"]:
                        scores.append(f"{inning.get('inning', '')}: {inning.get('r', 0)}/{inning.get('w', 0)} in {inning.get('o', 0)} overs")
                live_matches.append({
                    "team1": team1,
                    "team2": team2,
                    "team1_logo": team1_logo,
                    "team2_logo": team2_logo,
                    "status": status,
                    "venue": venue,
                    "match_type": match_type,
                    "scores": scores
                })
    return live_matches

def show_live_match_updates():
    """Fetch live match status and display in a visually appealing way."""
    live_matches = get_live_scores(selected_match_type)
    if not live_matches:
        st.info("No live matches at the moment.")
    else:
        for match in live_matches:
            status_class = get_status_class(match["status"])
            match_type_icon = get_match_type_icon(match["match_type"])
            # Highlight winner in status
            team1_disp = highlight_winner(match["team1"], match["status"])
            team2_disp = highlight_winner(match["team2"], match["status"])
            with st.expander(f"{match['team1']} vs {match['team2']} - {match['status']}", expanded=True):
                st.markdown(f"""
                    <div class="match-card">
                        <span class="match-badge">{match_type_icon} {match['match_type'].upper()}</span>
                        <span class="match-badge {status_class}">{match['status']}</span>
                        <div style="display:flex;align-items:center;justify-content:space-between;margin-top:10px;">
                            <div style="text-align:center;width:120px;">
                                <img src="{match['team1_logo']}" width="56" class="match-logo"/><br>
                                <span>{team1_disp}</span>
                            </div>
                            <div style="text-align:center;flex:1;">
                                <div class="match-teams">{team1_disp} <span style="color:#1f77b4;">VS</span> {team2_disp}</div>
                                <div class="match-venue">{match['venue']}</div>
                            </div>
                            <div style="text-align:center;width:120px;">
                                <img src="{match['team2_logo']}" width="56" class="match-logo"/><br>
                                <span>{team2_disp}</span>
                            </div>
                        </div>
                """, unsafe_allow_html=True)
                # Animated progress bars for runs (if available)
                for score in match["scores"]:
                    st.markdown(f'<div class="match-score">{score}</div>', unsafe_allow_html=True)
                    # Extract runs for progress bar (if possible)
                    import re
                    m = re.search(r':\s*(\d+)', score)
                    if m:
                        runs = int(m.group(1))
                        st.progress(min(runs / 400, 1.0))  # 400 as a max for cricket runs
                st.markdown("</div>", unsafe_allow_html=True)
                # You can add more details here (squads, toss, series, etc.) if available in your API

# Add a button to fetch and show live match updates
if st.button("Fetch Live Updates"):
    show_live_match_updates()

# Remove this block:
# st.subheader("Player Analytics")
# player_id = st.selectbox("Select Player", ["Player 1", "Player 2", "Player 3"], key="analytics_player_select")  # Simulate player selection
# player_analysis = PlayerAnalyzer.analyze_player(player_id)
# st.write(f"Player Analysis for {player_id}: {player_analysis}")

st.title("Fantasy Cricket Assistant")

# Example player data
player_data = {
    "Player 1": {
        "avatar": "assets/avatars/player1.png",
        "team_logo": "assets/logos/team1.png",
        "team_color": "#1f77b4",
        "stats": {"Runs": 450, "Wickets": 12, "Catches": 8}
    },
    "Player 2": {
        "avatar": "assets/avatars/player2.png",
        "team_logo": "assets/logos/team2.png",
        "team_color": "#ff7f0e",
        "stats": {"Runs": 320, "Wickets": 20, "Catches": 5}
    },
    "Player 3": {
        "avatar": "assets/avatars/player3.png",
        "team_logo": "assets/logos/team3.png",
        "team_color": "#2ca02c",
        "stats": {"Runs": 510, "Wickets": 8, "Catches": 10}
    }
}

# Add custom CSS for card styling at the top (only once)
st.markdown("""
    <style>
    .player-card {
        background: #23272f;
        border-radius: 16px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.2);
        padding: 24px;
        margin-bottom: 24px;
        text-align: center;
        display: inline-block;
        min-width: 300px;
    }
    .player-avatar {
        border-radius: 12px;
        margin-bottom: 12px;
    }
    .player-name {
        color: #fff;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .player-stats {
        color: #bbb;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)
# Player Analytics Card (fix empty box issue)
st.header("Player Analytics")
selected_player = st.selectbox("Select Player", list(player_data.keys()), key="avatar_player_select")
avatar_path = player_data[selected_player]["avatar"]
team_logo = player_data[selected_player]["team_logo"]
team_color = player_data[selected_player]["team_color"]
stats = player_data[selected_player]["stats"]

with st.container():
    st.markdown(f"""
        <div class="player-card" style="border: 3px solid {team_color};">
    """, unsafe_allow_html=True)
    st.image(avatar_path, width=100)
    st.image(team_logo, width=40)
    st.markdown(f"""
            <div class="player-name">{selected_player}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"<div class='player-stats'>Runs: {stats['Runs']}</div>", unsafe_allow_html=True)
    st.progress(min(stats['Runs'] / 600, 1.0))
    st.markdown(f"<div class='player-stats'>Wickets: {stats['Wickets']}</div>", unsafe_allow_html=True)
    st.progress(min(stats['Wickets'] / 50, 1.0))
    st.markdown(f"<div class='player-stats'>Catches: {stats['Catches']}</div>", unsafe_allow_html=True)
    st.progress(min(stats['Catches'] / 20, 1.0))

# --- Compare Players Section ---
st.header("Compare Players")
col1, col2 = st.columns(2)

player_keys = list(player_data.keys())
default_a = 0
default_b = 1 if len(player_keys) > 1 else 0

with col1:
    player_a = st.selectbox("Select Player A", player_keys, index=default_a, key="compare_a")
    avatar_a = player_data[player_a]["avatar"]
    team_logo_a = player_data[player_a]["team_logo"]
    stats_a = player_data[player_a]["stats"]
    st.image(avatar_a, width=80)
    st.image(team_logo_a, width=32)
    st.markdown(f"**{player_a}**")
    st.markdown(f"Runs: {stats_a['Runs']}  \nWickets: {stats_a['Wickets']}  \nCatches: {stats_a['Catches']}")

with col2:
    # Exclude player_a from the options for player_b if you want to prevent duplicates
    player_b_options = [p for p in player_keys if p != player_a] if len(player_keys) > 1 else player_keys
    # If player_a is the first, default to the next; else, default to the first
    default_b_index = 0 if player_a != player_keys[0] else 1 if len(player_keys) > 1 else 0
    player_b = st.selectbox("Select Player B", player_b_options, index=default_b_index, key="compare_b")
    avatar_b = player_data[player_b]["avatar"]
    team_logo_b = player_data[player_b]["team_logo"]
    stats_b = player_data[player_b]["stats"]
    st.image(avatar_b, width=80)
    if os.path.exists(team_logo_b):
        st.image(team_logo_b, width=32)
    else:
        st.write("(Team logo not found)")
    st.markdown(f"**{player_b}**")
    st.markdown(f"Runs: {stats_b['Runs']}  \nWickets: {stats_b['Wickets']}  \nCatches: {stats_b['Catches']}")

if player_a == player_b:
    st.warning("Please select two different players to compare.")

import numpy as np
labels = list(stats_a.keys())
values_a = list(stats_a.values())
values_b = list(stats_b.values())

fig, ax = plt.subplots()
x = np.arange(len(labels))
width = 0.35
ax.bar(x - width/2, values_a, width, label=player_a)
ax.bar(x + width/2, values_b, width, label=player_b)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel('Count')
ax.set_title('Player Comparison')
ax.legend()
st.pyplot(fig)

