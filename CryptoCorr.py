import ccxt
import pandas as pd
import numpy as np

# Initialize Binance USDT-M Futures exchange
exchange = ccxt.binanceusdm()

exchange
markets = exchange.fetch_markets()

# Filter symbols paired to USDT
usdt_symbols = [
    market["symbol"][:-5] for market in markets if market["quote"] == "USDT"
]

# Select top 200 symbols
symbols = usdt_symbols[:100]

symbols


def fetch_ohlcv(symbol, since, timeframe="1d"):
    """
    Fetch historical OHLCV data for a given symbol.
    """

    try:
        ohlcv = exchange.fetch_ohlcv(
            symbol, timeframe=timeframe, since=since, limit=1000
        )
        df = pd.DataFrame(
            ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
        )
        df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("datetime", inplace=True)
        return df["close"]
    except Exception as e:
        print(f"Could not fetch data for {symbol}: {e}")
        return None


def filter_and_save_correlations(correlations, threshold, output_file):
    """
    Filter symbols based on correlation threshold and save to a text file.
    """
    # Filter symbols with correlation higher than the threshold
    filtered_symbols = [
        symbol for symbol, corr in correlations.items() if corr > threshold
    ]
    # Format symbols to match the required text format
    formatted_symbols = ",".join(
        [
            f"BINANCE:{symbol.replace('/', '').replace('1000', '1000').replace('1M', '1M')}.P"
            for symbol in filtered_symbols
        ]
    )
    # Save to text file
    with open(output_file, "w") as file:
        file.write(formatted_symbols)
    print(f"{len(filtered_symbols)} filtered symbols saved to {output_file}")


# Fetch historical prices starting from January 1, 2023
price_data = {}
since = exchange.parse8601("2023-01-01T00:00:00Z")

for symbol in symbols:
    print(f"Fetching data for {symbol}")
    data = fetch_ohlcv(symbol, since)
    if data is not None:
        price_data[symbol] = data
# Create a DataFrame of prices and calculate daily returns
prices_df = pd.DataFrame(price_data)
prices_df = prices_df.dropna(axis=1, how="any")  # Remove symbols with insufficient data
returns_df = prices_df.pct_change().dropna()

returns_df
# Calculate correlation of each coin's returns with BTC
btc_returns = returns_df["BTC/USDT"]
correlations = {}
for symbol in returns_df.columns:
    corr = returns_df[symbol].corr(btc_returns)
    correlations[symbol] = corr

correlations
# Sort correlations in descending order
sorted_correlations = dict(
    sorted(correlations.items(), key=lambda item: item[1], reverse=True)
)

# Print correlations
print("\nCorrelation of each coin's returns with BTC:")
for symbol, corr in sorted_correlations.items():
    print(f"{symbol}: {corr:.4f}")
# Set correlation threshold and output file name
threshold = 0.6
output_file = "HighCorrelation.txt"

# Filter and save symbols with high correlation
filter_and_save_correlations(sorted_correlations, threshold, output_file)
