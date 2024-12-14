from portfolio_simulation import PortfolioSimulation
from config import parameter_variations
from cumulative_returns import create_cumulative_returns_table
from visualization import plot_cumulative_returns, plot_transition_matrix, plot_sampled_regimes
import pandas as pd
import openpyxl as px


def main():
    """
    Main function to run the portfolio simulation and save the results to an Excel file.
    """
    # Running base simulation
    simulation = PortfolioSimulation()
    base_performance = simulation.run_simulation()
    base_cumulative_returns = simulation.cumulative_returns*100

    # Running sensitivity analysis
    sensitivity_cumulative_returns = {label: returns * 100 for label, returns in
                                      simulation.sensitivity_analysis(parameter_variations).items()}

    # Summary DataFrames for performance metrics
    performance_df = pd.DataFrame(base_performance, index=[0])

    # Creating cumulative returns table
    cumulative_returns_table_df = create_cumulative_returns_table(base_cumulative_returns, sensitivity_cumulative_returns)

    # Summarized Regime Count
    regime_counts = simulation.df_returns["Regime"].value_counts().reindex(simulation.regimes)
    regime_counts_df = pd.DataFrame(regime_counts).reset_index()
    regime_counts_df.columns = ["Regime", "Count"]

    # Resampling the DataFrame to monthly frequency, picking the first day of each month
    sampled_returns_df = simulation.df_returns.resample('M').first()

    # Save the results to an Excel file with plots and matrices
    with pd.ExcelWriter('portfolio_simulation_results.xlsx', engine='openpyxl') as writer:
        performance_df.to_excel(writer, sheet_name='Base Performance Metrics', index=False)
        cumulative_returns_table_df.to_excel(writer, sheet_name='Cumulative Returns', index=False)
        regime_counts_df.to_excel(writer, sheet_name='Regime Counts', index=False)
        sampled_returns_df["Regime"].to_excel(writer, sheet_name='Sampled Regime Data', index=True)

        # Save transition matrix
        transition_matrix_df = pd.DataFrame(simulation.transition_matrix, columns=simulation.regimes, index=simulation.regimes)
        transition_matrix_df.to_excel(writer, sheet_name='Transition Matrix')

        # Plotting cumulative returns
        plot_cumulative_returns(base_cumulative_returns, sensitivity_cumulative_returns)
        workbook = writer.book
        worksheet = workbook['Cumulative Returns']
        img = px.drawing.image.Image('cumulative_returns_plot.png')
        worksheet.add_image(img, 'E5')

        # Additional visualizations
        plot_transition_matrix(simulation.transition_matrix, simulation.regimes)
        worksheet = workbook['Transition Matrix']
        img = px.drawing.image.Image('transition_matrix_plot.png')
        worksheet.add_image(img, 'E5')

        plot_sampled_regimes(simulation.df_returns, simulation.regimes)
        worksheet = workbook['Sampled Regime Data']
        img = px.drawing.image.Image('sampled_regimes_plot.png')
        worksheet.add_image(img, 'E5')

    # Remove the plot file after inserting into Excel
    import os
    os.remove('cumulative_returns_plot.png')
    os.remove('transition_matrix_plot.png')
    os.remove('sampled_regimes_plot.png')

if __name__ == "__main__":
    main()