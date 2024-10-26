import unittest
from unittest.mock import mock_open, patch

import pandas as pd
from src.main import (load_transactions_from_csv, load_transactions_from_json,
                      load_transactions_from_xlsx, main)


class TestTransactionLoader(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='[{"date": "2023-01-01", "state": "EXECUTED"}]')
    def test_load_transactions_from_json(self, mock_file):
        transactions = load_transactions_from_json("fake_path.json")
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['state'], "EXECUTED")

    @patch("builtins.open", new_callable=mock_open, read_data='transaction_date;transaction_description;state\n'
                                                              '2023-01-01;Sample transaction;EXECUTED')
    def test_load_transactions_from_csv(self, mock_file):
        transactions = load_transactions_from_csv("fake_path.csv")
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['state'], "EXECUTED")

    @patch("pandas.read_excel")
    def test_load_transactions_from_xlsx(self, mock_read_excel):
        mock_read_excel.return_value = pd.DataFrame({
            'Date': ['2023-01-01'],
            'Description': ['Sample transaction'],
            'FromAccount': ['Account 1'],
            'Amount': [100],
            'Currency': ['RUB'],
            'State': ['EXECUTED']
        })
        transactions = load_transactions_from_xlsx("fake_path.xlsx")
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['State'], "EXECUTED")

    @patch('builtins.input', side_effect=['1', 'EXECUTED', 'да', 'по убыванию', 'да', 'да', 'Sample'])
    @patch('builtins.print')
    @patch('src.main.load_transactions_from_json', return_value=[{
        'date': '2023-01-01',
        'description': 'Sample transaction',
        'state': 'EXECUTED',
        'from': 'Account 1',
        'operationAmount': {
            'amount': 100,
            'currency': {
                'code': 'RUB',
                'name': 'Российский рубль'
            }
        }
    }])
    def test_main(self, mock_load_json, mock_print, mock_input):
        main()
        mock_print.assert_any_call("Всего банковских операций в выборке: 1\n")
        mock_print.assert_any_call("2023-01-01 Sample transaction")
        mock_print.assert_any_call("Счет **Account 1")
        mock_print.assert_any_call("Сумма: 100 Российский рубль\n")


if __name__ == "__main__":
    unittest.main()
