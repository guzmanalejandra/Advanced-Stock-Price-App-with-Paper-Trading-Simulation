import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime

st.write("""
# Advanced Stock Price App with Paper Trading Simulation

This app displays **closing price**, **volume**, and a **candlestick chart** with technical indicators for your selected stock.  
Additionally, it includes a paper trading simulation based on a simple moving average strategy using historical data.
""")

# Sidebar for user inputs
st.sidebar.header('User Input Parameters')

tickerOptions = ['GOOGL', 'AAPL', 'MSFT', 'AMZN', 'TSLA']
selectedTicker = st.sidebar.selectbox('Select Stock Ticker', tickerOptions, index=0)

start_date = st.sidebar.date_input('Start Date', datetime.date(2010, 5, 31))
end_date = st.sidebar.date_input('End Date', datetime.date(2020, 5, 31))
if start_date > end_date:
    st.sidebar.error("Error: End date must fall after start date.")

ma_period = st.sidebar.slider('Moving Average Period (days)', min_value=5, max_value=200, value=20)

# Fetch stock data from yfinance
tickerData = yf.Ticker(selectedTicker)
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)

# Calculate the moving average for the closing price
tickerDf['MA'] = tickerDf['Close'].rolling(window=ma_period).mean()

# Use tabs to organize charts
tab1, tab2, tab3 = st.tabs(["Closing Price & MA", "Volume", "Candlestick Chart"])

with tab1:
    st.header("Closing Price with Moving Average")
    st.line_chart(tickerDf[['Close', 'MA']])
    
with tab2:
    st.header("Volume")
    st.line_chart(tickerDf['Volume'])

with tab3:
    st.header("Candlestick Chart")
    fig = go.Figure(data=[go.Candlestick(x=tickerDf.index,
                                          open=tickerDf['Open'],
                                          high=tickerDf['High'],
                                          low=tickerDf['Low'],
                                          close=tickerDf['Close'],
                                          name="Price")])
    fig.update_layout(xaxis_rangeslider_visible=False,
                      title=f'Candlestick Chart for {selectedTicker}',
                      xaxis_title='Date',
                      yaxis_title='Price (USD)')
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Raw Data")
st.dataframe(tickerDf)

csv = tickerDf.to_csv().encode('utf-8')
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name=f'{selectedTicker}_stock_data.csv',
    mime='text/csv',
)

st.write("---")
st.subheader("Paper Trading Simulation")

def simulate_trading(data, initial_capital=10000, shares_per_trade=1):
    cash = initial_capital
    shares = 0
    trades = []
    portfolio_values = []
    
    # Ensure data is sorted by date
    data = data.sort_index()
    
    for index, row in data.iterrows():
        # Generate trading signal based on moving average:
        # Buy if Close > MA, Sell if Close < MA
        if pd.isna(row['MA']):
            signal = 'hold'
        elif row['Close'] > row['MA']:
            signal = 'buy'
        elif row['Close'] < row['MA']:
            signal = 'sell'
        else:
            signal = 'hold'
        
        # If a buy signal occurs and we aren't holding any shares, execute a simulated buy.
        if signal == 'buy' and shares == 0:
            buy_price = row['Close']
            shares = shares_per_trade
            cash -= buy_price * shares
            trades.append({'Date': index, 'Action': 'Buy', 'Price': buy_price, 'Shares': shares})
        # If a sell signal occurs and we are holding shares, execute a simulated sell.
        elif signal == 'sell' and shares > 0:
            sell_price = row['Close']
            cash += sell_price * shares
            trades.append({'Date': index, 'Action': 'Sell', 'Price': sell_price, 'Shares': shares})
            shares = 0
        
        # Calculate current portfolio value (cash plus value of held shares)
        portfolio_value = cash + shares * row['Close']
        portfolio_values.append({'Date': index, 'Portfolio Value': portfolio_value, 'Cash': cash, 'Shares': shares})
    
    trades_df = pd.DataFrame(trades)
    portfolio_df = pd.DataFrame(portfolio_values).set_index('Date')
    return trades_df, portfolio_df

if st.button("Run Trading Simulation"):
    try:
        trades_df, portfolio_df = simulate_trading(tickerDf)
        st.write("### Trade History")
        st.dataframe(trades_df)
        st.write("### Portfolio Value Over Time")
        st.line_chart(portfolio_df['Portfolio Value'])
        final_value = portfolio_df['Portfolio Value'].iloc[-1]
        st.write(f"**Final Portfolio Value:** ${final_value:,.2f}")
    except Exception as e:
        st.error(f"Error during simulation: {e}")
