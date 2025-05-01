import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("final_cleaned_output.csv")
data["Filing Date"] = pd.to_datetime(data["Filing Date"])
data["Return Date"] = pd.to_datetime(data["Return Date"])

# App title
st.title("Annual 10-K Returns by Company")

# Sidebar: Single company selector
st.sidebar.header("Select a Company")
all_symbols = sorted(data["Symbol"].unique())
selected_symbol = st.sidebar.selectbox("Choose a company:", all_symbols)

# Bin color mapping
bin_colors = {
    1: "#ff0000",
    2: "#ffa700",
    3: "#fff400",
    4: "#a3ff00",
    5: "#2cba00"
}

# Custom labels for bin legend
bin_labels = {
    1: "Bin 1 (largest change in 10-K)",
    2: "Bin 2",
    3: "Bin 3",
    4: "Bin 4",
    5: "Bin 5 (smallest change in 10-K)"
}

if selected_symbol:
    fig, ax = plt.subplots(figsize=(10, 6))

    symbol_df = data[data["Symbol"] == selected_symbol]
    yearly = symbol_df.groupby("Year").agg({"Return": "mean", "Bins": "first"}).reset_index()
    yearly = yearly.sort_values("Year")

    # Plot colored segments by bin
    for i in range(len(yearly) - 1):
        x_vals = [yearly["Year"].iloc[i], yearly["Year"].iloc[i+1]]
        y_vals = [yearly["Return"].iloc[i], yearly["Return"].iloc[i+1]]
        bin_val = yearly["Bins"].iloc[i]
        color = bin_colors.get(bin_val, "#000000")
        ax.plot(x_vals, y_vals, color=color, linewidth=3)

    # Add dummy line for legend
    ax.plot([], [], label=selected_symbol, color="black")

    ax.set_title("Yearly Returns Around 10-K Filing", fontsize=16)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Return", fontsize=12)
    ax.legend(title="Company Symbol")
    ax.grid(True)

    # Year ticks: all gridlines, label every other year
    all_years = sorted(data["Year"].unique())
    ax.set_xticks(all_years)
    ax.set_xticklabels([str(y) if i % 2 == 0 else '' for i, y in enumerate(all_years)])

    st.pyplot(fig)

    # Show bin legend
    st.markdown("### Bin Color Legend")
    bin_legend = "  ".join(
        [f"<span style='color:{bin_colors[b]}; font-weight:bold;'>■</span> {bin_labels[b]}" for b in sorted(bin_colors)]
    )
    st.markdown(f"<div style='font-size:16px;'>{bin_legend}</div>", unsafe_allow_html=True)

else:
    st.info("Please select a company to view the chart.")
