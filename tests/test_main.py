import unittest

from main import filter_transactions_by_description, count_transactions_by_category, filter_by_currency


class TestTransactionFunctions(unittest.TestCase):
    def setUp(self):
        """Создаем тестовые данные для использования в тестах."""
        self.transactions = [
            {
                'description': 'Оплата за интернет',
                'operationAmount': {'amount': 100, 'currency': {'code': 'RUB', 'name': 'Российский рубль'}},
                'date': '2023-01-01',
                'from': 'Счет 1234'
            },
            {
                'description': 'Перевод другу',
                'operationAmount': {'amount': 200, 'currency': {'code': 'USD', 'name': 'Доллар США'}},
                'date': '2023-01-02',
                'from': 'Счет 5678'
            },
            {
                'description': 'Оплата за интернет',
                'operationAmount': {'amount': 150, 'currency': {'code': 'RUB', 'name': 'Российский рубль'}},
                'date': '2023-01-03',
                'from': 'Счет 1234'
            },
            {
                'description': 'Оплата за мобильную связь',
                'operationAmount': {'amount': 50, 'currency': {'code': 'RUB', 'name': 'Российский рубль'}},
                'date': '2023-01-04',
                'from': 'Счет 1234'
            }
        ]

    def test_filter_transactions_by_description(self):
        """Тест фильтрацию транзакций по описанию."""
        result = filter_transactions_by_description(self.transactions, 'интернет')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['description'], 'Оплата за интернет')
        self.assertEqual(result[1]['description'], 'Оплата за интернет')

    def test_count_transactions_by_category(self):
        """Тест подсчет транзакций по категориям."""
        result = count_transactions_by_category(self.transactions)
        self.assertEqual(result['Оплата за интернет'], 2)
        self.assertEqual(result['Перевод другу'], 1)
        self.assertEqual(result['Оплата за мобильную связь'], 1)

    def test_filter_by_currency(self):
        """Тест фильтрацию транзакций по валюте."""
        result = filter_by_currency(self.transactions, 'RUB')
        self.assertEqual(len(result), 3)
        self.assertTrue(all(t['operationAmount']['currency']['code'] == 'RUB' for t in result))


if __name__ == '__main__':
    unittest.main()
