from datetime import datetime
from logging_config import setup_logger


def mask_card(numbers_card_check: str) -> str:
    """Данная функция принимает номер банковской карты из
    16-ти цифр или
    20-ти значный номер счёта и возвращает отформатированный(замаскированный)номер
    карты или номер счёта
    Примеры входных данных:
        Maestro 1596837868705199
        Счет 64686473678894779589
        MasterCard 7158300734726758
        Счет 35383033474447895560
        Visa Classic 6831982476737658
        Visa Platinum 8990922113665229
        Visa Gold 5999414228426353
        Счет 73654108430135874305
    """
    logger = setup_logger('masks', 'masks.log')
    try:
        if len(numbers_card_check.split()[-1]) == 16:
            rep_symbol = ""
            mask = ""
            count = 0
            start = " ".join(
                numbers_card_check.split()[:-1]
            )  # Объединяем список обратно в строку
            number = numbers_card_check.split()[-1]

            for i in number:
                count += 1
                if 7 <= count <= 12:
                    i = "*"
                rep_symbol += i

            count = 0
            for i in rep_symbol:
                count += 1
                if count < 4:
                    mask += i
                else:
                    mask += i
                    mask += " "
                    count = 0
            mask = mask.rstrip()
            logger.info("ОК")

            return f"{start} {mask}"
        else:
            if len(numbers_card_check.split()[-1]) == 20:
                start = " ".join(numbers_card_check.split()[:-1])
                logger.info("ОК")
                return f"{start} **{numbers_card_check[-4:]}"
            else:
                logger.warning("Введён некорректный номер счёта или карты!")
                return "Введён некорректный номер счёта или карты!"



    except Exception as e:
        logger.error(f"Error: {e}")


def date(curr_date: str) -> str:
    """Функция принимающая дату формата типа '2018-07-11T02:26:18.671407'
    и преобразующая её в '11.07.18'.
    """
    date_input = datetime.strptime(curr_date, "%Y-%m-%dT%H:%M:%S.%f")
    date_output = datetime.strftime(date_input, "%d.%m.%y")
    return date_output


print(mask_card("Maestro 7863711"))
