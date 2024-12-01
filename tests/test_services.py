import unittest
import pandas as pd
import json
from src.services import analys_kashback, investment_bank, search_transactions_by_keyword, search_transactions_by_phone


class TestFinancialFunctions(unittest.TestCase):

    def setUp(self):
        # Подготовка тестовых данных
        self.data = pd.DataFrame({
            'Дата платежа': ['01.01.2021', '15.01.2021', '20.01.2021', '25.01.2021'],
            'Категория': ['Еда', 'Транспорт', 'Еда', 'Развлечения'],
            'Кэшбэк': [100, 200, 150, 0]
        })

        self.transactions = [
            {'Дата операции': '01.01.2021 12:00:00', 'Сумма операции': 1000, 'Описание': 'Покупка'},
            {'Дата операции': '15.01.2021 12:00:00', 'Сумма операции': 2000, 'Описание': 'Транспорт'},
            {'Дата операции': '20.01.2021 12:00:00', 'Сумма операции': 1500, 'Описание': 'Еда'},
            {'Дата операции': '25.01.2021 12:00:00', 'Сумма операции': -500, 'Описание': 'Возврат'}
        ]

    def test_analys_kashback(self):
        expected_output = {
            "Еда": 250,
            "Транспорт": 200
        }
        result = analys_kashback(self.data, 2021, 1)
        self.assertEqual(json.loads(result), expected_output)

    def test_analys_kashback_no_transactions(self):
        empty_data = pd.DataFrame(columns=['Дата платежа', 'Категория', 'Кэшбэк'])
        result = analys_kashback(empty_data, 2021, 1)
        self.assertEqual(result, json.dumps({}))

    def test_investment_bank(self):
        expected_savings = 150.0
        result = investment_bank('2021-01', self.transactions, 50)
        self.assertAlmostEqual(result, expected_savings)

    def test_investment_bank_no_transactions(self):
        result = investment_bank('2021-02', self.transactions, 100)
        self.assertEqual(result, 0.0)

    def test_search_transactions_by_keyword(self):
        keyword = 'покупка'  # Измените на слово, которое есть в описании
        expected_result = [
            {'Дата операции': '01.01.2021 12:00:00', 'Сумма операции': 1000, 'Описание': 'Покупка'},
        ]
        result = search_transactions_by_keyword(self.transactions, keyword)
        self.assertEqual(json.loads(result), expected_result)

    def test_search_transactions_by_phone(self):
        transactions_with_phone = [
            {'Дата операции': '01.01.2021', 'Сумма операции': 1000, 'Описание': 'Покупка +7 123 456-78-90'},
            {'Дата операции': '15.01.2021', 'Сумма операции': 2000, 'Описание': 'Транспорт'},
            {'Дата операции': '20.01.2021', 'Сумма операции': 1500, 'Описание': 'Еда +7 987 654-32-10'},
        ]
        expected_result = [
            {'Дата операции': '01.01.2021', 'Сумма операции': 1000, 'Описание': 'Покупка +7 123 456-78-90'},
            {'Дата операции': '20.01.2021', 'Сумма операции': 1500, 'Описание': 'Еда +7 987 654-32-10'},
        ]
        result = search_transactions_by_phone(transactions_with_phone)
        self.assertEqual(json.loads(result), expected_result)


if __name__ == '__main__':
    unittest.main()
