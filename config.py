n_periods = 500
n_assets = 3
regimes = ["Bullish", "Bearish", "Volatile"]

# Base simulation parameters
mean_returns = {
    "Bullish": [0.001, 0.0005, 0.0008],
    "Bearish": [-0.0002, 0.0003, 0.0004],
    "Volatile": [0.0005, 0.0002, 0.0006]
}
volatility = {
    "Bullish": [0.015, 0.005, 0.01],
    "Bearish": [0.02, 0.006, 0.012],
    "Volatile": [0.025, 0.008, 0.015]
}
# Sensitivity analysis parameters
parameter_variations = {
    "Higher Volatility": {
        "mean_returns": {
            "Bullish": [0.002, 0.0005, 0.001],
            "Bearish": [-0.0005, 0.0004, 0.0005],
            "Volatile": [0.001, 0.0003, 0.0008]
        },
        "volatility": {
            "Bullish": [0.025, 0.01, 0.015],
            "Bearish": [0.025, 0.008, 0.02],
            "Volatile": [0.035, 0.012, 0.025]
        }
    },
    "Lower Volatility": {
        "mean_returns": {
            "Bullish": [0.0008, 0.0004, 0.0006],
            "Bearish": [-0.0001, 0.0002, 0.0003],
            "Volatile": [0.0004, 0.0002, 0.0005]
        },
        "volatility": {
            "Bullish": [0.01, 0.003, 0.005],
            "Bearish": [0.015, 0.004, 0.007],
            "Volatile": [0.02, 0.005, 0.012]
        }
    }
}