from src.generators import (card_number_generator, filter_by_currency,
                            transaction_descriptions)


def test_filter_by_currency():
    transaction_data = [
        {
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Transaction 1",
        },
        {
            "operationAmount": {"currency": {"code": "EUR"}},
            "description": "Transaction 2",
        },
        {
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Transaction 3",
        },
    ]

    result = list(filter_by_currency(transaction_data, "USD"))

    assert len(result) == 2
    assert all(
        transaction["operationAmount"]["currency"]["code"] == "USD"
        for transaction in result
    )


def test_transaction_descriptions():
    transactions = [{"description": "Transaction 1"}, {"description": ""}, {}]

    result = list(transaction_descriptions(transactions))

    assert len(result) == 2
    assert "Transaction 1" in result
    assert "" in result


def test_card_number_generator():
    start_card = 123456
    num_cards = 3

    result = list(card_number_generator(start_card, start_card + num_cards))

    assert len(result) == num_cards


if __name__ == "__main__":
    test_filter_by_currency()
    test_transaction_descriptions()
    test_card_number_generator()
