import sqlite3
import os

DB_PATH = "e:/Fantasy-Cricket-Chatbot/Fantasy-Cricket-Chatbot/db/fantasy_teams.db"

def init_db():
    # Ensure the directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            user_id TEXT PRIMARY KEY,
            team TEXT,
            captain TEXT,
            vice_captain TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_team(user_id, team, captain, vice_captain):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('REPLACE INTO teams (user_id, team, captain, vice_captain) VALUES (?, ?, ?, ?)',
              (user_id, ",".join(team), captain, vice_captain))
    conn.commit()
    conn.close()

def load_team(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT team, captain, vice_captain FROM teams WHERE user_id=?', (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        team = row[0].split(",") if row[0] else []
        return team, row[1], row[2]
    return [], None, None