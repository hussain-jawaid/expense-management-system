import mysql.connector
from contextlib import contextmanager
from logging_setup import get_logger


logger = get_logger("db_helper", "db_helper.log")


@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor

    if commit:
        connection.commit()
    cursor.close()
    connection.close()


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with expense_date: {expense_date} amount: {amount} category: {category} notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )


def delete_expense_for_date(expense_date):
    logger.info(f"delete_expense_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))


def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with Start: {start_date}, End: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            """
            SELECT category, SUM(amount) as total 
            FROM expenses WHERE expense_date
            BETWEEN %s and %s  
            GROUP BY category;
            """, (start_date, end_date)
        )
        data = cursor.fetchall()
        return data

def fetch_monthly_expenses():
    logger.info(f"fetch_monthly_expenses called")
    with get_db_cursor() as cursor:
        cursor.execute(
            """
            SELECT 
            MONTHNAME(expense_date) AS month,
            SUM(amount) AS total_spent
            FROM expenses
            GROUP BY month
            ORDER BY month;
            """
        )
        monthly_expenses = cursor.fetchall()
        return monthly_expenses


if __name__ == '__main__':
    # get_db_cursor()
    # expenses = fetch_expenses_for_date("2024-08-01")
    # insert_expense("2024-08-25", 150, "Food", "Eat samosas")
    # delete_expense_for_date("2024-08-25")
    # summary = fetch_expense_summary("2024-08-01", "2024-08-05")
    monthly_expenses = fetch_monthly_expenses()
