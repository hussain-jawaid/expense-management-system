from fastapi import FastAPI, HTTPException
import db_helper
from datetime import date
from typing import List
from pydantic import BaseModel


app = FastAPI()


class Expense(BaseModel):
    amount: int
    category: str
    notes: str


class DateRange(BaseModel):
    start_date: date
    end_date: date


@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to fetch expenses from database.")
    return expenses


@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date, expenses: List[Expense]):
    db_helper.delete_expense_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)


@app.post("/category/analytics/")
def get_analytics_by_category(date_range: DateRange):
    summary = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
    if summary is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database.")
    return summary


@app.get("/monthly/analytics/")
def get_analytics_by_month():
    monthly_expenses = db_helper.fetch_monthly_expenses()
    if monthly_expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve monthly expenses from database.")
    return monthly_expenses