import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your data
data = pd.read_csv("final_cleaned_output.csv")
data["Filing Date"] = pd.to_datetime(data["Filing Date"])
data["Return Date"] = pd.to_datetime(data["Return Date"])

# Create month-level index for returns
data["YearMonth"] = data["Return Date"].dt.to_period("M").dt.to_timestamp()

# App title
st.title("Cosine Similarity vs Monthly Return Over Time")

# Company selection
symbols = sorted(data["Symbol"].unique())
selected_symbol = st.sidebar.selectbox("Choose a company:", symbols)

# Filter data for selected company
firm_df = data[data["Symbol"] == selected_symbol].copy()

# Group cosine similarity by filing month (one row per 10-K)
filing_series = firm_df.groupby("Filing Date")["Cosine Similarity"].first().sort_index()

# Group return by calendar month and smooth
monthly_return = firm_df.groupby("YearMonth")["Return"].mean().rolling(3, min_periods=1).mean()

# Plot
fig, ax1 = plt.subplots(figsize=(10, 6))

# Cosine Similarity line (blue)
ax1.plot(filing_series.index, filing_series.values, 'o-', color="blue", label="Cosine Similarity")
ax1.set_ylabel("Cosine Similarity", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")

# Secondary y-axis for return
ax2 = ax1.twinx()
ax2.plot(monthly_return.index, monthly_return.values, '-s', color="darkorange", label="Return (smoothed)")
ax2.set_ylabel("Return (%)", color="darkorange")
ax2.tick_params(axis="y", labelcolor="darkorange")

# Title and layout
plt.title(f"{selected_symbol} - Cosine Similarity & Returns Over Time")
fig.tight_layout()

st.pyplot(fig)

# Optional explanation or legend
st.markdown("**Note:** Cosine Similarity is based on filing date (blue), returns are monthly with 3-month smoothing (orange).")
