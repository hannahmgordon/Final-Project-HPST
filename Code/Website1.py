import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset once
@st.cache_data
def load_data():
    data = pd.read_csv("final_cleaned_output.csv")
    data["Filing Date"] = pd.to_datetime(data["Filing Date"])
    data["Return Date"] = pd.to_datetime(data["Return Date"])
    data["YearMonth"] = data["Return Date"].dt.to_period("M").dt.to_timestamp()
    return data

data = load_data()

# Load S&P 500 benchmark data
sp500 = pd.read_csv("SP500_historical.csv")
sp500["date"] = pd.to_datetime(sp500["date"])
sp500["Year"] = sp500["date"].dt.year
sp500.columns = sp500.columns.str.strip()
sp500 = sp500.rename(columns={"Return": "SP500_Return"})

# Custom CSS to improve sidebar styling
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            background-color: #001f3f;
        }
        .sidebar-content, .css-1d391kg, .css-1lcbmhc, .css-1v0mbdj {
            color: white !important;
        }
        .st-emotion-cache-1wmy9hl, .st-emotion-cache-1v0mbdj {
            color: white !important;
        }
        .stRadio > div {
            flex-direction: column;
            gap: 0.5em;
        }
        .stRadio > div > label {
            background-color: #001f3f;
            color: white;
            padding: 0.6em 1em;
            border-radius: 6px;
            transition: background-color 0.3s;
            cursor: pointer;
        }
        .stRadio > div > label:hover {
            background-color: #003366;
        }
        .stRadio > div > label[data-selected="true"] {
            background-color: #004080;
            color: white;
        }
        .block-container {
            padding-top: 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("", ["Home", "Annual Returns by Company", "10K Cosine Similarity vs Monthly Return Over Time", "Report"], key="nav")

# (The rest of the Streamlit code remains unchanged for each page section.)
