import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import yfinance as yf

st.set_page_config(page_title="S&P 500 App", page_icon="🎯")
st.title("S&P 500 App")
st.sidebar.header("User Input Features")

@st.cache_data
def load_data():
    df = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", header=0
    )
    return df[0]


def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'


def price_plot(symbol):
    df = pd.DataFrame(data[symbol].Close)
    df["Date"] = df.index
    fig = plt.figure()
    plt.fill_between(df.Date, df.Close, color="skyblue", alpha=0.3)
    plt.plot(df.Date, df.Close, color="skyblue", alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight="bold")
    plt.xlabel("Date", fontweight="bold")
    plt.ylabel("Closing Price", fontweight="bold")
    return st.pyplot(fig)


df = load_data()
sector = df.groupby("GICS Sector")
sorted_sector_unique = sorted(df["GICS Sector"].unique())
selected_sector = st.sidebar.multiselect(
    "Sector", sorted_sector_unique, sorted_sector_unique
)
df_selected_sector = df[(df["GICS Sector"].isin(selected_sector))]

st.subheader("Display Companies in Selected Sector")
st.write(
    f"Data Dimension: {str(df_selected_sector.shape[0])} rows and {str(df_selected_sector.shape[1])} columns."
)
st.dataframe(df_selected_sector)
st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)
data = yf.download(
    tickers=list(df_selected_sector[:10].Symbol),
    period="ytd",
    interval="1d",
    group_by="ticker",
    auto_adjust=True,
    prepost=True,
    threads=True,
    proxy=None,
)

num_company = st.sidebar.slider("Number of Companies", 1, 5)
if st.button("Show Plots"):
    st.header("Stock Closing Price")
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)
