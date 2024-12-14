import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_cumulative_returns(base_cumulative_returns, sensitivity_cumulative_returns):
    """
    Plots the cumulative returns over time for the base case and sensitivity cases.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(base_cumulative_returns, label='Base Case', color='blue')
    for label, metrics in sensitivity_cumulative_returns.items():
        plt.plot(metrics, label=label)
    plt.title('Cumulative Returns Over Time')
    plt.xlabel('Days')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.grid()
    plt.savefig('cumulative_returns_plot.png', bbox_inches='tight')
    plt.show()
    plt.close()

def plot_transition_matrix(transition_matrix, regimes):
    """
    Plots the regime transition probability matrix.
    """
    plt.figure(figsize=(8, 6))
    sns.heatmap(pd.DataFrame(transition_matrix, index=regimes, columns=regimes), annot=True, cmap="YlGnBu", fmt=".2f", cbar=True)
    plt.title("Regime Transition Probability Matrix")
    plt.xlabel("To Regime")
    plt.ylabel("From Regime")
    plt.savefig('transition_matrix_plot.png', bbox_inches='tight')
    plt.show()
    plt.close()

def plot_sampled_regimes(df_returns, regimes):
    """
    Plots the sampled regime transitions over time.
    """
    sampled_returns_df = df_returns.resample('M').first()
    regime_mapping = {regime: idx for idx, regime in enumerate(regimes)}
    color_mapping = {
        "Bullish": "green",
        "Bearish": "red",
        "Volatile": "orange"
    }
    plt.figure(figsize=(10, 6))
    colors = sampled_returns_df["Regime"].map(color_mapping)
    sns.scatterplot(x=sampled_returns_df.index, y=sampled_returns_df["Regime"].map(regime_mapping), marker='o',
                    palette=color_mapping, hue=sampled_returns_df["Regime"], legend=False, s=100, color=colors)
    plt.yticks(ticks=list(regime_mapping.values()), labels=list(regime_mapping.keys()))
    plt.title("Monthly Sampled Regime Transitions Over Time")
    plt.xlabel("Date")
    plt.ylabel("Regime")
    plt.savefig('sampled_regimes_plot.png', bbox_inches='tight')
    plt.grid()
    plt.show()
    plt.close()