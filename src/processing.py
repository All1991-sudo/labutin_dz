from datetime import datetime
from typing import List, Optional


def sorted_dict(data: List[dict], executed: Optional[bool]) -> List[dict]:
    """Функция принимает список словарей и по умолчанию возвращает только те,
    у которых ключе 'state' значение 'EXECUTED'. Если же передать в параметр executed
    значение False при вызове функции, вернутся списки со значением CANCELED в ключе
    'state'
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

def sorted_dict_to_time(date: List[dict], sorting: Optional[bool]) -> List[dict]:
    """Функция принимает список словарей, в котором есть дата формата iso 8601
    и сортирует список словарей по дате. (По умолчанию сортировка по убыванию).
    Если при вызове функции передать в параметр 'sorting' значение False, сортировка
    будеть по возростанию.
    """
    return sorted(
        date, key=lambda x: datetime.fromisoformat(x["date"]), reverse=sorting
    )
