from unittest.mock import patch, mock_open
import pandas as pd
from src.transaction_read import read_financial_operations_csv, read_financial_operations_excel


def test_read_financial_operations_csv():
    """
        Тест для функции read_financial_operations_csv.

        Проверяет, что функция правильно читает данные из CSV-файла и преобразует их
        в список словарей с полями 'date', 'amount', и 'description'.

        Использует mock для имитации чтения данных из CSV-файла.
    """
    mock_csv_data = "date,amount,description\n2024-08-01,100.00,Deposit\n2024-08-02,-50.00,Withdrawal\n"

    with patch("builtins.open", mock_open(read_data=mock_csv_data)):
        result = read_financial_operations_csv("fake_path.csv")
        expected = [
            {"date": "2024-08-01", "amount": "100.00", "description": "Deposit"},
            {"date": "2024-08-02", "amount": "-50.00", "description": "Withdrawal"}
        ]
        assert result == expected


def test_read_financial_operations_excel():
    """
        Тест для функции read_financial_operations_excel.

        Проверяет, что функция правильно читает данные из Excel-файла и преобразует их
        в список словарей с полями 'date', 'amount', и 'description'.

        Использует mock для имитации чтения данных из Excel-файла.
    """
    mock_excel_data = pd.DataFrame({
        "date": ["2024-08-01", "2024-08-02"],
        "amount": [100.00, -50.00],
        "description": ["Deposit", "Withdrawal"]
    })
    with patch("pandas.read_excel", return_value=mock_excel_data):
        result = read_financial_operations_excel("fake_path.xlsx")
        expected = [
            {"date": "2024-08-01", "amount": 100.00, "description": "Deposit"},
            {"date": "2024-08-02", "amount": -50.00, "description": "Withdrawal"}
        ]
        assert result == expected
