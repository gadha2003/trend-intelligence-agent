import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os

# Auto refresh safely (DO NOT use time.sleep + rerun)
from streamlit_autorefresh import st_autorefresh

# Refresh every 15 seconds
st_autorefresh(interval=15000, key="refresh")

# Force Unicode font support
matplotlib.rcParams['font.family'] = ['DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# Page config
st.set_page_config(
    page_title="Multi-Agent AI Trend Monitoring Dashboard",
    layout="wide"
)

# Animated Background
st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background-color: #000428;
}

/* Animated grid */
#grid-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 200vw;
    height: 200vh;
    pointer-events: none;
    z-index: 0;

    background-image:
        linear-gradient(rgba(0,255,255,0.2) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,255,0.2) 1px, transparent 1px);

    background-size: 50px 50px;

    animation: moveGrid 10s linear infinite;
}

@keyframes moveGrid {
    from {
        transform: translate(0px, 0px);
    }
    to {
        transform: translate(-50px, -50px);
    }
}

/* Content above background */
.main {
    position: relative;
    z-index: 1;
}

/* Neon Title */
h1 {
    color: cyan;
    text-shadow: 0 0 10px cyan, 0 0 20px cyan;
    text-align: center;
}

h2, h3 {
    color: cyan;
}

/* Table styling */
[data-testid="stDataFrame"] {
    background-color: rgba(0,0,0,0.6);
}

</style>

<div id="grid-bg"></div>
""", unsafe_allow_html=True)

# Title
st.title("Multi-Agent AI Trend Monitoring Dashboard")

# Check database exists
DB_FILE = "trends.db"

if not os.path.exists(DB_FILE):
    st.warning("Database not found yet. Agent may still be collecting data.")
    st.stop()

# Connect to database
conn = sqlite3.connect(DB_FILE)

# Load data
df = pd.read_sql_query(
    "SELECT topic, source, timestamp FROM trends ORDER BY timestamp DESC",
    conn
)

conn.close()

# Display data
if df.empty:

    st.warning("No data available yet.")

else:

    col1, col2 = st.columns(2)

    # Table
    with col1:

        st.subheader("Live Trends Feed")

        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True,
            height=400
        )

    # Chart
    with col2:

        st.subheader("Top Trend Frequency")

        trend_counts = df['topic'].value_counts().head(10)

        fig, ax = plt.subplots()

        trend_counts.plot(
            kind='bar',
            ax=ax,
            color='cyan'
        )

        ax.set_xlabel("Topic")
        ax.set_ylabel("Frequency")
        ax.tick_params(axis='x', rotation=45)

        st.pyplot(fig)

# Footer
st.markdown("---")
st.caption("Auto-refreshes every 15 seconds | Powered by Multi-Agent AI")
