import streamlit as st
import sqlite3
import time

# --- 1. PAGE CONFIG & CYBERPUNK STYLES ---
st.set_page_config(page_title="Vertigo Automation Suite", layout="centered")

# Custom CSS for Cyber Banking Vibe
st.markdown("""
    <style>
    /* Main Background and Text */
    .stApp {
        background-color: #0d0e15;
        color: #00ffcc;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Subtitles and secondary text */
    .cyber-sub {
        color: #8892b0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Customizing Streamlit Inputs */
    div.stNumberInput input {
        background-color: #1a1c29 !important;
        color: #00ffcc !important;
        border: 1px solid #00ffcc !important;
    }
    
    /* Button Base Styling */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    /* Cyan Button (Add) */
    div[data-testid="stHorizontalBlock"] div:nth-of-type(1) button {
        background-color: #00ffcc !important;
        color: #0d0e15 !important;
        border: 1px solid #00ffcc !important;
        box-shadow: 0 0 10px #00ffcc;
    }
    
    /* Red Button (Deduct) */
    div[data-testid="stHorizontalBlock"] div:nth-of-type(2) button {
        background-color: #ff3366 !important;
        color: #ffffff !important;
        border: 1px solid #ff3366 !important;
        box-shadow: 0 0 10px #ff3366;
    }
    
    /* visible/Blend Button (Reset) */
    div[data-testid="stHorizontalBlock"] div:nth-of-type(3) button {
        background-color: transparent !important;
        color: #8892b0 !important; /* Matches background exactly to stay slightly invisible */
        border: 1px solid transparent !important;
        box-shadow: none !important;
    }
    div[data-testid="stHorizontalBlock"] div:nth-of-type(3) button:hover {
        background-color: #1a1c29 !important; /* Changes slightly on hover so users can find it */
        color: #8892b0 !important; 
    }
    
    /* Custom Yellow Text for Alerts */
    .cyber-yellow {
        color: #ffcc00;
        font-weight: bold;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE INITIALIZATION ---
def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_current_balance():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT TOTAL(amount) FROM inventory')
    balance = c.fetchone()[0]
    conn.close()
    return int(balance)

def update_balance(val):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('INSERT INTO inventory (amount) VALUES (?)', (val,))
    conn.commit()
    conn.close()

def reset_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('DELETE FROM inventory')
    conn.commit()
    conn.close()

# --- 3. SESSION STATE MANAGEMENT (NAVIGATION) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- PAGE 1: HOME ---
if st.session_state.page == 'home':
    st.title("Vertigo Automation Suite")
    st.markdown('<p class="cyber-sub">A lightweight, offline-ready layout designed to keep local businesses running 24/7.</p>', unsafe_allow_html=True)
    
    st.write(" ")
    st.write(" ")
    slide = st.slider("slide left to continue", min_value=0, max_value=100, value=0)
    
    if slide >= 80:
        st.session_state.page = 'main'
        st.rerun()

# --- PAGE 2: MAIN INVENTORY ---
elif st.session_state.page == 'main':
    if st.button("⬅ Exit Suite", key="exit"):
        st.session_state.page = 'home'
        st.rerun()
        
    st.header("⚡ Cyber Banking Terminal")
    
    current_bal = get_current_balance()
    st.metric(label="CURRENT SECURE BALANCE", value=f"${current_bal}")

    # Text Input with input verification
    user_input = st.text_input("Enter Integer Amount:", value="")
    
    input_valid = False
    clean_val = 0
    
    if user_input:
        if user_input.isdigit():
            clean_val = int(user_input)
            input_valid = True
        else:
            st.error("🚨 please input numbers only")

    # Three buttons in series with explicit text labels
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Add Amount") and input_valid:
            msg_slot = st.empty()
            
            msg_slot.markdown('<p class="cyber-yellow">⚠️ cutting off connection to simulate offline-first mode</p>', unsafe_allow_html=True)
            time.sleep(2)
            
            msg_slot.markdown('<p class="cyber-yellow">💾 saving into database until connection is restored</p>', unsafe_allow_html=True)
            update_balance(clean_val)
            time.sleep(2)
            
            msg_slot.markdown('<p class="cyber-yellow">🔄 connection restored, syncing to the cloud</p>', unsafe_allow_html=True)
            time.sleep(1.5)
            msg_slot.empty()
            st.rerun()
            
    with col2:
        if st.button("Deduct Amount") and input_valid:
            update_balance(-clean_val)
            st.success(f"Deducted ${clean_val} successfully.")
            st.rerun()
            
    with col3:
        # This button contains text but the button is masked via CSS to blend entirely with the background
        if st.button("Reset Amount"):
            reset_db()
            st.toast("Database cleared.")
           
# Footer Credits
st.write("---")
st.markdown("""
    <p style='font-family: "Share Tech Mono", monospace; color: #64748b; text-align: center;'>
    Copyright © 2026 | Code by Vertigo Software
    </p>
""", unsafe_allow_html=True)
  
