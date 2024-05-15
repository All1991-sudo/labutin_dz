from datetime import datetime
def date(curr_date: str) -> str:
    """ Функция принимающая дату формата типа '2018-07-11T02:26:18.671407' 
    и преобразующая её в '11.07.18'.
    """
    date_input = datetime.strptime(curr_date, "%Y-%m-%dT%H:%M:%S.%f")
    date_output = datetime.strftime(date_input, "%d.%m.%y")
    return date_output
