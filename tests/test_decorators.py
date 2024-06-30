from src.decorators import log


# Тесты для декоратора log
def test_log_decorator_without_output():
    @log
    def multiply(a, b):
        return a * b

    assert multiply(3, 5) == 15


def test_log_decorator_with_output():
    mock_output_file = "test_log_output.txt"

    @log(output=mock_output_file)
    def divide(a, b):
        return a / b

    # Вызываем функцию
    divide(10, 2)

    # Проверяем, что результат записался в файл
    with open(mock_output_file, "r") as file:
        content = file.read()
        assert "Функция divide ok" in content


def test_log_decorator_exception_handling():
    mock_output_file = "test_log_output.txt"

    @log(output=mock_output_file)
    def greet(name):
        print("Inside greet function")
        return "Hello, " + name

    # Тестируем, что исключение обрабатывается и записывается в файл
    greet(123)  # Вызываем функцию с некорректным параметром

    with open(mock_output_file, "r") as file:
        content = file.read()
        assert "greet error: TypeError. Inputs: (123,), {}" in content


# Запуск тестов
test_log_decorator_without_output()
test_log_decorator_with_output()
test_log_decorator_exception_handling()

print("All tests passed successfully!")
