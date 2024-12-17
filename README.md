# Crypto Correlation Calculator

A Python script that calculates the correlation between various cryptocurrencies and Bitcoin (BTC) using historical price data from Binance Futures. The script filters cryptocurrencies based on a specified correlation threshold and exports a list formatted for use in TradingView.

---

## Features

- **Fetch Historical Data**: Retrieves historical closing price data for a list of selected cryptocurrencies from Binance USDT-M Futures.
- **Calculate Correlations**: Computes the Pearson correlation coefficient between each cryptocurrency's returns and BTC's returns.
- **Filter by Threshold**: Allows users to set a correlation threshold to filter cryptocurrencies that are highly correlated with BTC.
- **Export to TradingView**: Generates a formatted list of symbols that can be directly imported into TradingView's watchlists or indicators.

---

## Usage

### Install Dependencies

Ensure you have Python 3.x installed. Install the required libraries using pip:

```bash
pip install ccxt pandas numpy
```

### Configure Parameters

- Symbol List: Modify the symbols list in the script to add or remove cryptocurrencies.
- Correlation Threshold: Set the threshold variable in the script to your desired correlation value (e.g., 0.6).

## Run the Script

Execute the script from the command line:

```bash
python crypto_correlation_calculator.py
```

## Output

- The script prints the correlation coefficients in the console.
- It generates an output file named HighCorrelation.txt containing the list of filtered symbols formatted for TradingView.

## Example Output

An example of the formatted output list:

```bash
BINANCE:ETHUSDT.P,BINANCE:DOGEUSDT.P,BINANCE:BCHUSDT.P,BINANCE:SOLUSDT.P,BINANCE:RUNEUSDT.P,BINANCE:NEARUSDT.P,BINANCE:BNBUSDT.P,BINANCE:1000SHIBUSDT.P,BINANCE:AVAXUSDT.P,BINANCE:OPUSDT.P,BINANCE:APTUSDT.P,BINANCE:1000FLOKIUSDT.P,BINANCE:IMXUSDT.P,BINANCE:1000PEPEUSDT.P,BINANCE:FILUSDT.P,BINANCE:INJUSDT.P,BINANCE:ARBUSDT.P,BINANCE:ATOMUSDT.P,BINANCE:THETAUSDT.P,BINANCE:GALAUSDT.P,BINANCE:ADAUSDT.P,BINANCE:ICPUSDT.P,BINANCE:SEIUSDT.P,BINANCE:FTMUSDT.P,BINANCE:UNIUSDT.P
```

## How It Works

1. **Data Fetching**: Utilizes the ccxt library to fetch daily historical closing prices for each symbol starting from a specified date.
2. **Data Processing**: Calculates daily returns and handles missing data by dropping incomplete datasets.
3. **Correlation Calculation**: Computes the correlation coefficients between each cryptocurrency’s returns and BTC’s returns.
4. **Filtering and Exporting**: Filters out symbols below the correlation threshold and formats the remaining symbols into a string compatible with TradingView.

## Requirements

- Python 3.x
- Libraries:
    - ccxt
    - pandas
    - numpy

## Customization

- Adjust Timeframe: Modify the `since` variable to change the start date for historical data.
- Change Time Intervals: Alter the `timeframe` parameter in the `fetch_ohlcv` function to use different candle intervals (e.g., '1h' for hourly data).
- Modify Symbols: Update the symbols list to include additional cryptocurrencies available on Binance USDT-M Futures.

