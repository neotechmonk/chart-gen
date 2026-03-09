"""Entry point for chart_gen package."""

from pathlib import Path

from .engine import run_engine

if __name__ == "__main__":
    tickers = [
        "MSFT",
        "AAPL",
        "GOOGL",
        "AMZN",
        "META",
        "NVDA",
        "TSLA",
        "JPM",
        "V",
        "JNJ",
        "UNH",
    ]
    out = Path(__file__).resolve().parents[2] / "output"
    out.mkdir(parents=True, exist_ok=True)
    run_engine(symbol=tickers, output_dir=out)
