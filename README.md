# Advanced Stock Price App with Paper Trading Simulation

This repository contains a Streamlit app that provides advanced stock price visualizations and a paper trading simulation based on a simple moving average strategy. The app uses historical data fetched from [yfinance](https://pypi.org/project/yfinance/) and offers interactive charts and a trading simulation framework.

## Features

- **Interactive User Inputs:**  
  - Select stock ticker from a preset list (e.g., GOOGL, AAPL, MSFT, AMZN, TSLA).
  - Choose a custom date range for historical data.
  - Adjust the moving average period using a slider.

- **Visualizations:**  
  - **Closing Price & Moving Average:** Displays a line chart of the closing price alongside its moving average.
  - **Volume Chart:** Shows the trading volume over time.
  - **Candlestick Chart:** Provides an interactive candlestick chart using Plotly.
  - **Raw Data Table:** View and download the raw historical stock data as CSV.

- **Paper Trading Simulation:**  
  - Simulates buy/sell signals based on the closing price relative to its moving average.
  - Tracks a simulated portfolio (starting with \$10,000) and displays trade history.
  - Displays the evolution of the portfolio value over time.

## Installation

### Prerequisites

- Python 3.7 or higher
- [pip](https://pip.pypa.io/en/stable/)

### Required Python Libraries

- [yfinance](https://pypi.org/project/yfinance/)
- [streamlit](https://pypi.org/project/streamlit/)
- [pandas](https://pypi.org/project/pandas/)
- [plotly](https://pypi.org/project/plotly/)

![image](https://github.com/user-attachments/assets/5335f0af-088a-402c-8556-5968cdd8cdb6)


You can install the required libraries using pip:

```bash
pip install yfinance streamlit pandas plotly



