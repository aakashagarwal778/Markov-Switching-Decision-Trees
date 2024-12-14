# Dynamic Portfolio Allocation Using Markov-Switching Decision Trees: A Regime-Driven Investment Framework

## Description
This program implements a dynamic portfolio allocation strategy using Markov-Switching Decision Trees to adapt to different market regimes.

## Files:

### 1. **portfolio_simulation.py**  
   Contains the `PortfolioSimulation` class, which runs the portfolio simulation, performs sensitivity analysis, and generates the required performance metrics.

### 2. **config.py**  
   Defines the `parameter_variations` used in the sensitivity analysis for portfolio simulation.

### 3. **cumulative_returns.py**  
   Provides the function `create_cumulative_returns_table` to generate a table of cumulative returns for both base and sensitivity simulations.

### 4. **visualization.py**  
   Contains functions to plot and save visualizations, including cumulative returns, transition matrix, and regime data.

### 5. **main.py**  
   The entry point of the program. It runs the portfolio simulation, performs sensitivity analysis, generates performance metrics, creates visualizations, and saves all results to an Excel file.

## Purpose  
This framework allows for an investment strategy that dynamically adjusts to changing market conditions, providing regime-based portfolio allocations and insights through simulations, metrics, and visualizations.
