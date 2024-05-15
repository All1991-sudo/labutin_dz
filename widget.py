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

    if len(numbers_card_check.split()[-1]) == 16:
        start = ""
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

        return f"{start} {mask}"
    else:
        if len(numbers_card_check.split()[-1]) == 20:
            start = " ".join(numbers_card_check.split()[:-1])
            return f"{start} **{numbers_card_check[-4:]}"
        else:
            return "Введён некорректный номер счёта или карты!"


result = mask_card("Visa Gold 12345678451545781234")
print(result)
