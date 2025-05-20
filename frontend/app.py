import streamlit as st
from add_update import add_update_tab
from analytics_by_category import category_analytics
from analytics_by_month import monthly_analytics


st.title("Expense Management System")

tab1, tab2, tab3 = st.tabs(["Add/Update", "Category Analytics", "Monthly Analytics"])

with tab1:
    add_update_tab()
with tab2:
    category_analytics()
with tab3:
    monthly_analytics()