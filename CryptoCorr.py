import ccxt
import pandas as pd


def initialize_exchange():
    return ccxt.binanceusdm()


def fetch_price_data(exchange, symbols, since):
    price_data = {}
    for symbol in symbols:
        print(f"Fetching data for {symbol}")
        try:
            ohlcv = exchange.fetch_ohlcv(
                symbol, timeframe="1d", since=since, limit=1000
            )
            df = pd.DataFrame(
                ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
            )
            df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms")
            df.set_index("datetime", inplace=True)
            price_data[symbol] = df["close"]
        except Exception as e:
            print(f"Could not fetch data for {symbol}: {e}")
    return price_data


def categorize_symbols_by_correlation(correlations, thresholds):
    categorized = {f"Correlation >= {threshold}": [] for threshold in thresholds}

    for symbol, corr in correlations.items():
        for threshold in thresholds:
            if corr >= threshold:
                categorized[f"Correlation >= {threshold}"].append(symbol)
                break

    return categorized


def save_to_file(categorized_symbols, output_file):
    with open(output_file, "w") as file:
        for label, symbols in categorized_symbols.items():
            file.write(f"### {label}\n")
            formatted = ",".join(
                [f"BINANCE:{symbol.replace('/', '')}.P" for symbol in symbols]
            )
            file.write(formatted + "\n\n")
    print(f"Symbols saved to {output_file}")


if __name__ == "__main__":
    exchange = initialize_exchange()
    markets = exchange.fetch_markets()
    
    markets = markets[:500]
    
    usdt_symbols = []

    for market in markets:
        if market["quote"] == "USDT":
            symbol = market["symbol"]
            try:
                ticker = exchange.fetch_ticker(symbol)
                if ticker and ticker.get("baseVolume") and ticker.get("last"):
                    volume = int(ticker["baseVolume"] * ticker["last"] // 1_000_000)

                    if volume > 20:
                        # usdt_symbols.append({"Symbol": symbol[:-5], "Volume": volume})
                        usdt_symbols.append(symbol[:-5])

            except Exception as e:
                print(f"Error fetching ticker for {symbol}: {e}")

    since = exchange.parse8601("2023-01-01T00:00:00Z")
    price_data = fetch_price_data(exchange, usdt_symbols, since)

    prices_df = pd.DataFrame(price_data).dropna(axis=1, how="any")
    returns_df = prices_df.pct_change().dropna()

    btc_returns = returns_df["BTC/USDT"]
    correlations = {
        symbol: returns_df[symbol].corr(btc_returns) for symbol in returns_df.columns
    }

    sorted_correlations = dict(
        sorted(correlations.items(), key=lambda item: item[1], reverse=True)
    )

    thresholds = [0.7, 0.65, 0.6]
    categorized_symbols = categorize_symbols_by_correlation(
        sorted_correlations, thresholds
    )

    save_to_file(categorized_symbols, "TradingViewSymbols.txt")
