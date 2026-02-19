import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates

# MarketWatch-style theme
sns.set_theme(style="whitegrid", context="talk")

pred_np = predictions.numpy()
test_df = df.iloc[split_idx:].copy()
test_dates = test_df.index
test_prices = test_df["Close"]

# Define "today" marker (you can replace with pd.Timestamp("today"))
today = test_dates[int(len(test_dates) * 0.95)]

fig = plt.figure(figsize=(22, 16))
gs = fig.add_gridspec(4, 1, height_ratios=[3, 3, 1.5, 1.5], hspace=0.35)

# ============================================
# 1. REAL-TIME / HISTORICAL PRICE PANEL
# ============================================
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(df.index, df["Close"], color="black", linewidth=2)
ax1.set_title("Real-Time / Historical Price", fontsize=18)
ax1.set_ylabel("Price")
ax1.grid(alpha=0.3)

# ============================================
# 2. PREDICTION PANEL
# ============================================
ax2 = fig.add_subplot(gs[1, 0])
ax2.plot(test_dates, test_prices, color="black", linewidth=2)

# Vertical “today” line
ax2.axvline(today, color="blue", linestyle="--", linewidth=2)

# Shade predicted regimes AFTER today
for date, pred in zip(test_dates, pred_np):
    if date < today:
        continue

    if pred == 1:
        ax2.axvspan(date - pd.Timedelta(hours=12),
                    date + pd.Timedelta(hours=12),
                    color="green", alpha=0.20)
    elif pred == 2:
        ax2.axvspan(date - pd.Timedelta(hours=12),
                    date + pd.Timedelta(hours=12),
                    color="red", alpha=0.20)

# Legend
green_patch = mpatches.Patch(color='green', alpha=0.25, label='Predicted Easy (GREEN)')
red_patch   = mpatches.Patch(color='red',   alpha=0.25, label='Predicted Hard (RED)')
today_line  = mpatches.Patch(color='blue', alpha=0.6, label='Today')

ax2.legend(handles=[green_patch, red_patch, today_line], loc="upper left")
ax2.set_title("Model Prediction (Liquidity Regimes)", fontsize=18)
ax2.set_ylabel("Price")
ax2.grid(alpha=0.3)

# ============================================
# 3. VOLATILITY PANEL
# ============================================
ax3 = fig.add_subplot(gs[2, 0], sharex=ax2)
ax3.plot(test_dates, test_df["volatility"], color="purple", linewidth=1.8)
ax3.set_title("Rolling Volatility (10‑day)", fontsize=16)
ax3.set_ylabel("Volatility")
ax3.grid(alpha=0.3)

# ============================================
# 4. AMIHUD PANEL
# ============================================
ax4 = fig.add_subplot(gs[3, 0], sharex=ax2)
ax4.plot(test_dates, test_df["amihud"], color="darkorange", linewidth=1.8)
ax4.set_title("Amihud Illiquidity (Liquidity Stress)", fontsize=16)
ax4.set_ylabel("Illiquidity")
ax4.set_xlabel("Date")
ax4.grid(alpha=0.3)

# Format x-axis
ax4.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax4.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

plt.tight_layout()
plt.show()
