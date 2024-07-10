from unittest.mock import mock_open, patch

from src.utils import load_transactions


def test_file_not_exist():
    assert load_transactions('nonexistent.json') == []


def test_file_exist_but_not_list():
    with patch('builtins.open', mock_open(read_data='{"key": "value"}')):
        assert load_transactions('dummy.json') == []


def test_file_exist_with_list():
    data = '[{"transaction_id": "1", "amount": "100"}]'
    with patch('builtins.open', mock_open(read_data=data)):
        with patch('os.path.exists', return_value=True):
            assert load_transactions('dummy.json') == [{"transaction_id": "1", "amount": "100"}]


def test_json_decode_error():
    with patch('builtins.open', mock_open(read_data='not a json')):
        with patch('os.path.exists', return_value=True):
            assert load_transactions('dummy.json') == []


def run_tests():
    test_file_not_exist()
    test_file_exist_but_not_list()
    test_file_exist_with_list()
    test_json_decode_error()


# Run tests
run_tests()
