from backend import db_helper
from datetime import date


def test_fetch_expenses_for_date():
    expenses = db_helper.fetch_expenses_for_date("2024-08-01")
    assert expenses[0]["expense_date"] == date(2024, 8, 1)
    assert expenses[0]["amount"] == 1227.0
    assert expenses[0]["category"] == "Rent"
    assert expenses[0]["notes"] == "Monthly rent payment"


def test_insert_expense():
    db_helper.insert_expense("2024-08-25", 300, "Food", "Eat tasty samosas")
    expenses = db_helper.fetch_expenses_for_date("2024-08-25")
    assert expenses[0]["expense_date"] == date(2024, 8, 25)
    assert expenses[0]["amount"] == 300
    assert expenses[0]["category"] == "Food"
    assert expenses[0]["notes"] == "Eat tasty samosas"


def test_delete_expense_for_date():
    db_helper.delete_expense_for_date("2024-08-25")
    expenses = db_helper.fetch_expenses_for_date("2024-08-25")
    assert len(expenses) == 0


def test_fetch_expense_summary_invalid_range():
    summary = db_helper.fetch_expense_summary("2055-08-01", "2065-08-05")
    assert len(summary) == 0

