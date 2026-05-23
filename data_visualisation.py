import streamlit as st
import pandas as pd
from plotnine import *

st.title("Media Rhetoric Surrounding Trump and Daily Oil Price Movements During the US–Iran Conflict")

oil = pd.read_csv("/Users/alvinwang/Desktop/daily_oil_price.csv")
rhetoric = pd.read_csv("/Users/alvinwang/Desktop/daily_rhetoric.csv")
event_window = pd.read_csv("/Users/alvinwang/Desktop/event_window_rhetoric.csv")
event_summary = pd.read_csv("/Users/alvinwang/Desktop/event_summary_rhetoric.csv")
event_oil = pd.read_csv("/Users/alvinwang/Desktop/event_oil_price.csv")

oil["date"] = pd.to_datetime(oil["date"])
rhetoric["date"] = pd.to_datetime(rhetoric["date"])
event_summary["date"] = pd.to_datetime(event_summary["date"])

oil = oil.sort_values("date").reset_index(drop=True)
oil["return"] = oil["close"].pct_change()

oil_cols_to_round = ["open", "high", "low", "close"]
oil[oil_cols_to_round] = oil[oil_cols_to_round].round(3)

st.subheader("Data Viewer")
selected_data = st.multiselect(
    "Select data to view:",
    options=["Daily Oil Price", "Daily Rhetoric", "Event Window", "Event Summary", "Event Oil Price"],
    default=[]
)

if "Daily Oil Price" in selected_data:
    st.write("### Daily Oil Price Data")
    st.dataframe(oil)

if "Daily Rhetoric" in selected_data:
    st.write("### Daily Rhetoric Data")
    st.dataframe(rhetoric)

if "Event Window" in selected_data:
    st.write("### Event Window Rhetoric Data")
    st.dataframe(event_window)

if "Event Summary" in selected_data:
    st.write("### Event Summary Rhetoric Data")
    st.dataframe(event_summary)

if "Event Oil Price" in selected_data:
    st.write("### Event Oil Price Data")
    st.dataframe(event_oil)

st.subheader("Data Visualization")
selected_plots = st.multiselect(
    "Select plots to view:",
    options=["Price plot", "Returns plot", "Rhetoric index"],
    default=[]
)

event_dates = event_summary["date"].dropna().unique()
color_list = ["red", "red", "red", "red", "blue", "blue", "red", "blue", "red", "red"]

if "Price plot" in selected_plots:
    st.write("### Price Plot (Oil Close Price over Time)")
    plot1 = (ggplot(oil, aes(x="date", y="close")) 
          + geom_line(color="black") 
          + geom_vline(xintercept=event_dates, color=color_list, linetype="dashed", alpha=0.7)
          + theme_minimal()
          + labs(title="Daily Oil Close Price", x="Date", y="Close Price"))
    st.pyplot(ggplot.draw(plot1))

if "Returns plot" in selected_plots:
    st.write("### Returns Plot (Daily Oil Price Return)")
    plot2 = (ggplot(oil.dropna(subset=["return"]), aes(x="date", y="return")) 
          + geom_line(color="black") 
          + geom_vline(xintercept=event_dates, color=color_list, linetype="dashed", alpha=0.7)
          + theme_minimal()
          + labs(title="Daily Oil Price Returns", x="Date", y="Return"))
    st.pyplot(ggplot.draw(plot2))

if "Rhetoric index" in selected_plots:
    st.write("### Rhetoric Index (Political Rhetoric Index over Time)")
    plot3 = (ggplot(rhetoric, aes(x="date", y="rhetoric_index")) 
          + geom_line(color="black") 
          + geom_vline(xintercept=event_dates, color=color_list, linetype="dashed", alpha=0.7)
          + theme_minimal()
          + labs(title="Daily Political Rhetoric Index", x="Date", y="Rhetoric Index"))
    st.pyplot(ggplot.draw(plot3))
