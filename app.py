# Neurowake - Streamlit single-file app
# Save this as neurowake_streamlit_app.py and run with:
#    pip install streamlit numpy pandas
#    streamlit run neurowake_streamlit_app.py

import streamlit as st
import numpy as np
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="NEUROWAKE", layout="wide", initial_sidebar_state="collapsed")

# ---------- Styles ----------
APP_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

:root{
  --bg1: #061f4e; /* deep blue */
  --bg2: #123881; /* lighter blue */
  --accent1: #e12cfc; /* purple */
  --accent2: #23cdfa; /* aqua-ish */
}
html, body, [class*="css"], .stApp {
  height: 100%;
  margin: 0;
  font-family: 'Inter', sans-serif;
  background: linear-gradient(180deg, var(--bg1) 0%, var(--bg2) 100%);
}

/* futuristic glass cards */
.card {
  background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02));
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 8px 30px rgba(2,6,23,0.5);
  border: 1px solid rgba(255,255,255,0.05);
  backdrop-filter: blur(6px) saturate(120%);
}

.header-title {
  font-size: 42px;
  font-weight: 800;
  letter-spacing: 1px;
  color: white;
  margin: 0;
  padding: 0;
  text-transform: uppercase;
  line-height: 1;
  text-shadow: 0 4px 28px rgba(33,12,80,0.55);
}

.header-date {
  font-size: 14px;
  color: rgba(255,255,255,0.8);
  margin-top: 6px;
}

.accent-pill {
  display: inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  font-weight: 600;
  background: linear-gradient(90deg, var(--accent1), var(--accent2));
  color: white;
  box-shadow: 0 6px 18px rgba(33,12,80,0.36);
}

.metric-title {
  color: rgba(255,255,255,0.85);
  font-weight: 600;
}

.small-muted {
  color: rgba(255,255,255,0.7);
  font-size: 13px;
}

.button-neon {
  background: linear-gradient(90deg, var(--accent1), var(--accent2));
  color: #fff !important;
  border: none;
  padding: 10px 18px;
  border-radius: 10px;
  font-weight: 700;
}

.footer-note {
  color: rgba(255,255,255,0.65);
  font-size: 12px;
}

/* make streamlit's default containers a bit tighter */
.css-1d391kg .stButton>button { height: 44px; }
"""

st.markdown(f"<style>{APP_CSS}</style>", unsafe_allow_html=True)

# ---------- Header ----------
now = datetime.now()
datestr = now.strftime('%A, %B %d, %Y')

header_col1, header_col2 = st.columns([3,1])
with header_col1:
    st.markdown(f"<div class='card'><div style='display:flex;align-items:center;justify-content:space-between'>"
                f"<div>"
                f"<h1 class='header-title'>neurowake</h1>"
                f"<div class='header-date'>{datestr}</div>"
                f"</div>"
                f"</div></div>", unsafe_allow_html=True)
with header_col2:
    st.markdown("<div style='height:100%'></div>", unsafe_allow_html=True)

st.write("\n")

# ---------- Main UI ----------
main_left, main_right = st.columns([2,1])

# --- Left: Predictions & Chander ---
with main_left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div style='display:flex;justify-content:space-between;align-items:center'>"
                "<div>"
                "<div class='metric-title'>AI sleep predictions</div>"
                "</div>"
                "<div class='accent-pill'>beta</div>"
                "</div>", unsafe_allow_html=True)

    # random predictions
    seed = random.randint(0, 999999)
    random_state = np.random.RandomState(seed)
    sleep_score = int(random_state.uniform(45, 98))
    total_sleep = round(random_state.uniform(4.0, 9.5), 1)
    deep_sleep = round(total_sleep * random_state.uniform(0.12, 0.28), 1)
    rem_sleep = round(total_sleep * random_state.uniform(0.18, 0.35), 1)
    sleep_latency = int(random_state.uniform(5, 40))

    c1, c2, c3 = st.columns(3)
    c1.metric("Sleep Score", f"{sleep_score}", delta=f"{int(sleep_score- (50 + random_state.uniform(-5,5)))}")
    c2.metric("Total Sleep (hrs)", f"{total_sleep}")
    c3.metric("Deep (hrs) / REM (hrs)", f"{deep_sleep} / {rem_sleep}")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.progress(min(max(sleep_score/100, 0.0), 1.0))

    # Random 'chander' - interpreted as lunar/moon-themed -- a short poetic label for tonight.
    lunar_names = [
        "Lunar Drift",
        "Moonthread",
        "Silver Tide",
        "Nocturne Veil",
        "Selenic Whisper",
        "Quiet Crescent",
        "Midnight Lattice",
        "Celestial Sigh",
        "Indigo Hush",
        "Tide of Stars"
    ]
    chander_pick = random.choice(lunar_names)
    st.markdown(f"<h3 style='margin-top:12px'>{chander_pick}</h3>", unsafe_allow_html=True)

    st.markdown("<hr style='opacity:0.12'/>", unsafe_allow_html=True)

    # small table of mock nightly breakdown
    breakdown = pd.DataFrame({
        'stage': ['Light', 'Deep', 'REM', 'Awake'],
        'hours': [round(total_sleep - deep_sleep - rem_sleep,1), deep_sleep, rem_sleep, round(random_state.uniform(0.05,0.4),1)]
    })
    st.table(breakdown)

    st.markdown("</div>", unsafe_allow_html=True)

# --- Right: Sleep Feedback ---
with main_right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='metric-title'>Sleep feedback</div>", unsafe_allow_html=True)

    quality = st.slider('How would you rate your sleep quality last night?', 0, 100, 72)
    duration = st.number_input('How many hours did you sleep?', min_value=0.0, max_value=24.0, value=total_sleep, step=0.25)
    sleep_notes = st.text_area('Notes (what woke you, dreams, noises, comfort...)', placeholder='I woke twice, dreams about...')

    submitted = st.button('Submit feedback', key='submit_feedback')
    if submitted:
        st.success('Thanks — feedback received.')
        # show minimal summarized feedback
        st.markdown(f"**Quality:** {quality} / 100  ")
        st.markdown(f"**Duration:** {duration} hrs  ")
        if sleep_notes.strip():
            st.markdown(f"**Notes:** {st.session_state.get('last_notes', sleep_notes)}")
        # save to session (lightweight local storage)
        st.session_state['last_feedback'] = {'quality': quality, 'duration': duration, 'notes': sleep_notes, 'timestamp': datetime.now().isoformat()}
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

# ---------- Footer / Small extras ----------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div style='display:flex;justify-content:space-between;align-items:center'>"
                "<div><span class='footer-note'>Neurowake — mock AI sleep tool · UI theme: blue → purple gradients</span></div>"
                "<div><small class='small-muted'>seed: " + str(seed) + "</small></div>"
                "</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- End ----------

# Notes for the developer/user:
# - The color scheme variables are declared at the top of the CSS under :root.
# - To change the base gradient, edit --bg1 and --bg2. For detail accents, edit --accent1 and --accent2.
# - Predictions are mock/random. Replace the random sections with your model outputs where noted.
