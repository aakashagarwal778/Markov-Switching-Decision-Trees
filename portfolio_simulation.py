import numpy as np # comment
import pandas as pd # added another comment
from sklearn.tree import DecisionTreeRegressor
import pandas as pd
from sklearn.tree import DecisionTreeRegressor # added another - another comment
from config import n_periods, n_assets, regimes, mean_returns, volatility

class PortfolioSimulation:
    """
    A class to run a simulation of a portfolio applying MSM for regime detection and decision trees for portfolio allocation.
    """
    def __init__(self):
        self.n_periods = n_periods
        self.n_assets = n_assets
        self.regimes = regimes
        self.mean_returns = mean_returns
        self.volatility = volatility

        # Initialize a random transition matrix
        self.transition_matrix = np.random.rand(3, 3)
        # Normalize rows to sum to 1 ensuring valid probabilities distribution
        self.transition_matrix /= self.transition_matrix.sum(axis=1, keepdims=True)

    def run_simulation(self):
        """
        Run a simulation of the portfolio returns based on the given parameters.
        """
        np.random.seed(42)
        asset_returns = np.zeros((self.n_periods, self.n_assets))
        regime_states = np.zeros(self.n_periods, dtype=int)
        current_regime = 0
        for t in range(self.n_periods):
            mean = self.mean_returns[self.regimes[current_regime]]
            vol = self.volatility[self.regimes[current_regime]]
            asset_returns[t, :] = np.random.normal(mean, vol)
            regime_states[t] = current_regime
            current_regime = np.random.choice([0, 1, 2], p=self.transition_matrix[current_regime])
        dates = pd.date_range(start="2020-01-01", periods=self.n_periods, freq="D")
        self.df_returns = pd.DataFrame(asset_returns, columns=["Stocks", "Bonds", "Commodities"], index=dates)
        self.df_returns["Regime"] = [self.regimes[i] for i in regime_states]
        self.refine_transition_matrix(regime_states)
        _, portfolio_returns = self.apply_decision_tree()
        performance_metrics = self.calculate_performance(portfolio_returns)

        return performance_metrics

    def refine_transition_matrix(self, regime_states):
        """
        Refine the transition matrix based on the observed regime states.
        """
        num_iterations = 100
        for _ in range(num_iterations):
            transition_counts = np.zeros((len(self.regimes), len(self.regimes)))
            for (i, j) in zip(regime_states[:-1], regime_states[1:]):
                transition_counts[i, j] += 1
            self.transition_matrix = (transition_counts.T / transition_counts.sum(axis=1)).T

    def apply_decision_tree(self):
        """
        Apply a decision tree regressor to predict the portfolio allocations for each regime.
        """
        epsilon = 1e-8
        trees = {regime: DecisionTreeRegressor(max_depth=3) for regime in self.regimes}
        portfolio_returns = np.zeros(self.n_periods)
        for regime in self.regimes:
            regime_data = self.df_returns[self.df_returns["Regime"] == regime][
                ["Stocks", "Bonds", "Commodities"]].values

            X = np.zeros((regime_data.shape[0] - 1, 4))
            y = np.zeros((regime_data.shape[0] - 1, 3))

            for i in range(1, regime_data.shape[0]):
                X[i - 1] = np.concatenate([regime_data[i - 1], [self.regimes.index(regime)]])

                # Normalize the next period's returns to create allocations
                next_returns = regime_data[i]
                allocation_sum = np.sum(next_returns)
                y[i - 1] = next_returns / allocation_sum

            trees[regime].fit(X, y)

        # generate portfolio allocations and compute returns
        for t in range(1, self.n_periods):
            current_regime = self.df_returns["Regime"].iloc[t]
            tree = trees[current_regime]

            previous_data = self.df_returns.iloc[t - 1, :3].values
            input_data = np.concatenate([previous_data, [self.regimes.index(current_regime)]])
            predicted_allocation = tree.predict([input_data])[0]
            predicted_allocation = np.maximum(predicted_allocation, 0)

            allocation_sum = np.sum(predicted_allocation)
            if allocation_sum > epsilon:
                predicted_allocation /= allocation_sum  # Normalize to sum to 1
            else:
                print(f"Warning: Allocation sum is zero for period {t}, regime {current_regime}. Using equal allocation as fallback.")
                # predicted_allocation = np.ones_like(predicted_allocation) / len(predicted_allocation)

            portfolio_returns[t] = np.dot(predicted_allocation, self.df_returns.iloc[t, :3].values)

        return trees, portfolio_returns

    def calculate_performance(self, portfolio_returns):
        """
        Calculate the performance metrics of the portfolio simulation with constrained allocations.
        """
        self.cumulative_returns = portfolio_returns.cumsum()
        mean_return = np.mean(portfolio_returns)
        volatility = np.sqrt(np.mean(np.square(portfolio_returns - mean_return)))
        sharpe_ratio = mean_return / volatility

        cumulative_max = np.maximum.accumulate(self.cumulative_returns)
        drawdowns = self.cumulative_returns - cumulative_max
        max_drawdown = drawdowns.min()

        var_value = np.percentile(portfolio_returns, 5)

        result = {
            "Mean Daily Return": mean_return,
            "Volatility": volatility,
            "Sharpe Ratio": sharpe_ratio,
            "Maximum Drawdown": max_drawdown,
            "Final Cumulative Returns": self.cumulative_returns[-1],
            "Value at Risk (VaR, 95%)": var_value
        }
        return result

    def sensitivity_analysis(self, parameter_variations):
        """
        Perform a sensitivity analysis by varying the mean returns and volatility of the assets.
        """
        cumulative_returns_list = {}
        for label, params in parameter_variations.items():
            original_mean_returns = self.mean_returns.copy()
            original_volatility = self.volatility.copy()
            self.mean_returns = params["mean_returns"]
            self.volatility = params["volatility"]
            self.run_simulation()
            cumulative_returns_list[label] = self.cumulative_returns
            self.mean_returns = original_mean_returns
            self.volatility = original_volatility
        return cumulative_returns_list