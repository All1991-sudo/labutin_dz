import functools


def log(func=None, output=None):
    """
        Декоратор для логирования вызовов функций.

        Args:
        func: Функция, которую необходимо залогировать.
        output: Путь к файлу журнала для записи логов. Если не указан, логи не будут записываться в файл.


        Если передан output:
        * Пишет в файл сообщение о вызове функции, если он завершился без ошибок.
        * Пишет в файл сообщение об ошибке, если функция завершилась с ошибкой.

        Если output не передан:
        * Выводит сообщение о вызове функции в стандартный вывод (print), если он завершился без ошибок.
        * Выводит сообщение об ошибке в стандартный вывод (print), если функция завершилась с ошибкой.
        """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                start = f"Функция {func.__name__} ok"
                result = func(*args, **kwargs)
                log_message = f"{start}\n"
                if output:
                    with open(output, "a+") as file:
                        file.write(log_message)
                return result

            except Exception as e:
                error_message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"
                print(error_message)
                if output:
                    with open(output, "a") as file:
                        file.write(error_message)
                return ""

        return wrapper

    if func:
        return decorator(func)
    else:
        return decorator
