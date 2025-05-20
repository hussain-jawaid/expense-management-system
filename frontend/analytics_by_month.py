import streamlit as st
import requests
import pandas as pd


API_URL = "http://localhost:8000"

def monthly_analytics():
    response = requests.get(f"{API_URL}/monthly/analytics/")
    if response.status_code == 200:
        monthly_expenses = response.json()
    else:
        monthly_expenses = []
        st.error("Failed to fetch monthly expenses!")

    st.title("Expense Breakdown By Month")
    df = pd.DataFrame(monthly_expenses)
    st.bar_chart(df.set_index("month")["total_spent"])

    df = df.sort_values(by="total_spent", ascending=False)
    st.dataframe(df, hide_index=True)
