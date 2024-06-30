from datetime import datetime
from typing import List, Optional


def sorted_dict(data: List[dict], executed: Optional[bool] = True) -> List[dict]:
    """Функция sorted_dict осуществляет фильтрацию списка словарей по значению ключа "state".

    Args:
    data (List[dict]): Список словарей, который требуется отфильтровать.
    executed (Optional[bool]): Параметр, указывающий требуется ли выводить только выполненные элементы.
    По умолчанию установлен в True, что означает, что по умолчанию будут возвращены только выполненные элементы.

    Returns:
            List[dict]: Отфильтрованный список словарей, содержащий только те элементы,
                        у которых ключ "state" соответствует заданному условию.

    Примеры использования:
        data = [
            {"state": "EXECUTED", "value": 42},
            {"state": "CANCELED", "value": 37},
            {"state": "CANCELED", "value": 58}]

        sorted_dict(data)
        [{'state': 'EXECUTED', 'value': 42}]

        sorted_dict(data, executed=False)
        [{'state': 'CANCELED', 'value': 58}]

    Функция sorted_dict итерирует по каждому элементу в списке словарей и добавляет элемент в результирующий список,
    если значение ключа "state" соответствует указанному условию. Если executed установлено в True,
    будут возвращены только элементы, где "state" равен "EXECUTED". Если executed установлено в False,
    будут возвращены только элементы, где "state" равен "CANCELED".
    """
    result = []
    for i in data:
        for k, v in i.items():
            if k == "state":
                if v == "EXECUTED" and executed:
                    result.append(i)
                else:
                    if not executed and v == "CANCELED":
                        result.append(i)
    return result


def sorted_dict_to_time(date: List[dict], sorting: Optional[bool] = True) -> List[dict]:
    """Функция принимает список словарей, в котором есть дата формата iso 8601
    и сортирует список словарей по дате. (По умолчанию сортировка по убыванию).
    Если при вызове функции передать в параметр 'sorting' значение False, сортировка
    будеть по возростанию.
    """
    return sorted(
        date, key=lambda x: datetime.fromisoformat(x["date"]), reverse=sorting
    )
