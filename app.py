import streamlit as st
from datetime import date
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
from streamlit_option_menu import option_menu
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Stock Analysis", page_icon=":chart_with_upwards_trend:")

st.title("Stocks Analysis")
st.write("Stock Price Analysis and Price forecasting of National Stock Exchange (NSE).")
st.write("---")

# nifty stats
nifty = yf.Ticker('^NSEI') 
current = nifty.history(period='1d')['Close'].iloc[-1]
last = nifty.history(period='2d')['Close'].iloc[-2]
change = current-last 
per = (change / last) * 100

with st.sidebar:
    selected=option_menu(
    menu_title="Menu",
    options=["HOME","DATA","GRAPHS","FORECAST","HELP"],)
    st.write("---")
    
    st.subheader(f'NIFTY 50 = ₹ {round(current, 2)}')
    
    if change > 0:
        st.write(f'₹ + {round(change, 2)} (+{round(per, 2)}%) 🢁')
    else:
        st.write(f'₹ {round(change, 2)} ({round(per, 2)}%)🢃')
    st.write("---")

# nifty 50 company list
code = ("", "^NSEI", "ADANIPORTS.NS", "ASIANPAINT.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BHARTIARTL.NS", "BPCL.NS", "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DIVISLAB.NS", "DRREDDY.NS", "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS", "HDFC.NS", "HDFCBANK.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "INDUSINDBK.NS", "INFY.NS", "IOC.NS", "ITC.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS", "M&M.NS", "MARUTI.NS", "NESTLEIND.NS", "NTPC.NS", "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS", "SHREECEM.NS", "SUNPHARMA.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "TCS.NS", "TECHM.NS", "TITAN.NS", "ULTRACEMCO.NS", "UPL.NS", "WIPRO.NS")
company = ("", "Nifty 50 Index", "Adani Ports and Special Economic Zone Limited", "Asian Paints Limited", "Axis Bank Limited", "Bajaj Auto Limited", "Bajaj Finance Limited", "Bajaj Finserv Limited", "Bharti Airtel Limited", "Bharat Petroleum Corporation Limited", "Britannia Industries Limited", "Cipla Limited", "Coal India Limited", "Divi's Laboratories Limited", "Dr. Reddy's Laboratories Limited", "Eicher Motors Limited", "Grasim Industries Limited", "HCL Technologies Limited", "Housing Development Finance Corporation Limited", "HDFC Bank Limited", "Hindalco Industries Limited", "Hindustan Unilever Limited", "ICICI Bank Limited", "IndusInd Bank Limited", "Infosys Limited", "Indian Oil Corporation Limited", "ITC Limited", "JSW Steel Limited", "Kotak Mahindra Bank Limited", "Larsen & Toubro Limited", "Mahindra & Mahindra Limited", "Maruti Suzuki India Limited", "Nestle India Limited", "NTPC Limited", "Oil and Natural Gas Corporation Limited", "Power Grid Corporation of India Limited", "Reliance Industries Limited", "SBI Life Insurance Company Limited", "State Bank of India", "Shree Cement Limited", "Sun Pharmaceutical Industries Limited", "Tata Motors Limited", "Tata Steel Limited", "Tata Consultancy Services Limited", "Tech Mahindra Limited", "Titan Company Limited", "UltraTech Cement Limited", "UPL Limited", "Wipro Limited")

list=[x.lower() for x in company]
stocks=tuple(list)
selected_stocks = st.selectbox("\n\nSearch for NIFTY 50 Company",company)
p=selected_stocks
selected_stocks=selected_stocks.lower()
n=stocks.index(selected_stocks)
selected_stocks=code[n]

if n>0:
 st.subheader(f" {company[n]} ({code[n]})")  
 
 if selected_stocks:
     # current stats
     selected_stock = yf.Ticker(selected_stocks)
     current_price = selected_stock.history(period='1d')['Close'].iloc[-1]
     st.write(f'Current price = ₹ {round(current_price, 2)}')
     last_price = selected_stock.history(period='2d')['Close'].iloc[-2]
     change = current_price-last_price
     per = (change / last_price) * 100
     if change > 0:
         st.write(f'₹ + {round(change, 2)} (+{round(per, 2)}%) 🢁')
     else:
         st.write(f'₹ {round(change, 2)} ({round(per, 2)}%)🢃')
         
st.write("---")

# downloading data from yahoo finance 
def load_data(ticker):
    data = yf.download(ticker, START, END)
    data.reset_index(inplace=True)
    return data

if selected_stocks:
    
    if selected=="HOME":
        
        # time period
        START='2010-01-01'
        END = date.today().strftime("%Y-%m-%d")
    
        data = load_data(selected_stocks)
        
        # showing company stats
        
        closing = selected_stock.history(period='2d')['Close'].iloc[-2]
        st.write(f'Closing Price = ₹ {round(closing, 2)}')
        opening = selected_stock.history(period='1d')['Open'].iloc[-1]
        st.write(f'Opening Price = ₹ {round(opening, 2)}')
        
        h = selected_stock.history(period='1d')['High'].iloc[-1]
        l = selected_stock.history(period='1d')['Low'].iloc[-1]
        st.write(f'Days Range = ₹ {round(l, 2)} - ₹ {round(h, 2)}')
        
        Fhigh = selected_stock.history(period='252d')['High'].max()
        Flow = selected_stock.history(period='252d')['Low'].min()
        st.write(f' 52 Week Low - High = ₹{round(Flow,2)} - ₹{round(Fhigh,2)}')
        
        v = selected_stock.history(period='1d')['Volume'].iloc[-1]
        st.write(f'Volume = {v}')
        
        # price graph
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Price"))
        fig.layout.update(title_text="Price Graph", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)
   
    # company data
    
    if selected=='DATA':
        
        # time period
        TODAY = date.today().strftime("%Y-%m-%d")
        st.write("You can select time period of data ")
        START = st.date_input('Enter start date', value=pd.to_datetime('2023-01-01'))
        END = st.date_input('Enter end date', value=pd.to_datetime(date.today().strftime("%Y-%m-%d")))
        st.write("---")
        
        # loading data
        data_load_state = st.text("Loading data......")
        data = load_data(selected_stocks)
        data_load_state.text("Data loaded")
   
        st.subheader(f"Data of {p}")
        data = data.drop("Adj Close", axis=1)
        data.index = pd.to_datetime(data.index, infer_datetime_format=True)
        data.index = data.index.tz_localize('UTC')
        
        K=True
        st.write("Click here to view Data")
        if st.button("Full Data"):
            st.write(data)
            if st.button("Exit"):
                K = False
        n = st.text_input("Enter number of data to display")
        col1,col2,col3=st.columns(3)
        with col1:
            button1=st.button(f"First {n} Data")
        with col2:
            button2=st.button(f"Last {n} Data")
        X = True
        st.write("Click to view data")
        if button1:
            st.write(data.head(int(n)))
            if st.button("Exit "):
                X = False
        if button2:
            st.write(data.tail(int(n)))
            if st.button("Exit  "):
                X = False
        
        st.write("---")
    
    # Graph plotting
    
    if selected=="GRAPHS":
        
        st.subheader("GRAPHS")
        TODAY = date.today().strftime("%Y-%m-%d")
        st.write("You can select time period of Graph ")
        START = st.date_input('Enter start date', value=pd.to_datetime('2023-01-01'))
        END = st.date_input('Enter end date', value=pd.to_datetime(date.today().strftime("%Y-%m-%d")))
        
        data_load_state = st.text("Loading data......")
        data = load_data(selected_stocks)
        data_load_state.text("Data loaded")
    
        st.write("Click to preview Graph")
        col4,col5,col6=st.columns(3)
        with col4:
           button3=st.button("Opening and Closing Prices")
        with col5:
           button4=st.button("Low and High")
        with col6:
            button5=st.button("Volume")
        T=True
        if button3:
            st.write("Prices v/s Time")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="Opening Price"))  
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Closing Price"))
            fig.layout.update(title_text="Opening and Closing Prices", xaxis_rangeslider_visible=True)
            st.plotly_chart(fig)  
            if st.button("Exit    "):
                T=False            
        U=True  
        if button4:
            st.write("Prices v/s Time")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['Date'], y=data['High'], name="High"))  
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Low'], name="Low"))
            fig.layout.update(title_text="Low and High Prices", xaxis_rangeslider_visible=True)
            st.plotly_chart(fig)
            if st.button("Exit     "):
                U=False                
        V=True
        if button5:
            st.write("Volumes v/s Time")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Volume'], name="Volume"))
            fig.layout.update(title_text="Volume", xaxis_rangeslider_visible=True)
            st.plotly_chart(fig)
            if st.button("Exit      "):
                V=False
        
        st.write("---")
   
    
    if selected=="FORECAST":
            
        n_years = st.slider ("Years Of Prediction : ",1, 3)
        period = n_years*365

        START="2015-01-01"
        END=date.today().strftime("%Y-%m-%d")
        
        data_load_state = st.text("Loading data......")
        data = load_data(selected_stocks)
        data_load_state.text("Data loaded")
    
        # training data with prophet
        df_train = data[['Date','Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
        
        # forecasting data
        m = Prophet()
        m.fit(df_train)
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)  
    
        st.subheader("Forecast Data")
        
        forecast1=forecast.rename(columns={'ds':'Date','yhat':'Predicted Prices','yhat_lower':'Predicted Lowest','yhat_upper':'Predicted Highest','weekly':'Weekly','yearly':'Yearly'})
        forelist=['Date','Predicted Prices','Predicted Lowest','Predicted Highest','Weekly','Yearly']
        
        # forecasted dataframe
        st.write(forecast1[forelist])
        st.write('---')
        st.subheader("Prediction in Interval of Time")
        
        # forcasted data in time period
        Start = st.date_input('Enter start date',value=None)
        End=st.date_input('Enter End date',value=None)
        if(Start!=End):
            selected_forecast=forecast1.loc[(forecast1['Date']>pd.to_datetime(Start))&(forecast1['Date']<=pd.to_datetime(End))]
            st.write(selected_forecast[forelist])
        st.write("---")
        
       #Forcast plotting
        
        st.subheader('Forecasted Data Graphs')
        st.write("Actaul Prices v/s Predicted Prices")
        
        # actual vs predicted graph
        fig1 = plot_plotly(m, forecast)
        fig1.update_layout(xaxis_rangeslider_visible=False)
        st.plotly_chart(fig1)
        
        # forcast components graphs
        st.write("Forecast Components")
        fig2 = m.plot_components(forecast)
        st.write(fig2)
        st.write("---")
else:
    st.write("This tool allow users to visualize and analyze the stock prices of different companies and predict their future performance based on various factors.\n\nUser can see various graphs and future predicted prices of NIFTY 50 Companies.\n\nThis a useful tool for investors and traders to make informed decisions about their investments and gain insights into the stock market trends.")
    
if selected=="HELP":
    st.write("---")
    st.subheader("Help")
    st.write("Here you can see how to use stock analysis and prediction.\n\nSearch for a comapny and you can see it's current stats.\n\nMenu on the left can be used for various features. User can select to see Data, Graphs, Forecasted data through this menu.User can use given buttons options to get more information.\n\nForecast section shows the predicted values of the model with graphs for better understanding and analysis of stock prices of a company.\n\nTHANK YOU VISIT AGAIN!")
    st.write("Contact us :-\n\nIn case of any inconvienience or any issue, Report at Email : - abhinavkumarsingh96@gmail.com")