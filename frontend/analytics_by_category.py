import streamlit as st
from datetime import date
import requests
import pandas as pd


API_URL = "http://localhost:8000"

def category_analytics():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start date", date(2024, 8, 1))
    with col2:
        end_date = st.date_input("End date", date(2024, 8, 5))

    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
        }

        response = requests.post(f"{API_URL}/category/analytics/", json=payload)

        if response.status_code == 200:
            summary = response.json()
        else:
            summary = []
            st.error("Failed to fetch expenses!")

        df = pd.DataFrame(summary)
        total_sum = df["total"].sum()
        df["percentage"] = (df["total"] / total_sum * 100).round(1).astype(str) + "%"

        st.title("Expense Breakdown By Category")
        st.bar_chart(df.set_index("category")["total"])

        df = df.sort_values(by="total", ascending=False)
        st.dataframe(df, hide_index=True)
