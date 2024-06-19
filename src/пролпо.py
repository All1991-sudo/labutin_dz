# def generate_num_card(start, end):
#    if str(start).isdigit():
#        for _ in range(end):
#            str_num = f"{start:016}"
#            full_num = " ".join([str_num[x:x + 4] for x in range(0, len(str_num), 4)])
#            yield full_num
#            start += 1


# def create_counter():  # Внешняя функция
#    count = [0]
#
#    def counter():  # Внутренняя увеличивающая счётчик на 1
#        count[0] += 1
#        return count[0]
#
#    return counter
#
#
# my_counter = create_counter()
# print(my_counter())
# print(my_counter())
# print(my_counter())
# print(my_counter())
# print(my_counter())
# print(my_counter())


# from time import time
#
#
# def timer(func):
#    def wrapper(*args, **kwargs):
#        time_1 = time()
#        result = func(*args, **kwargs)
#        time_2 = time()
#        print(f" Rime for work: {time_2 - time_1}")
#
#    return wrapper
#
#
# @timer
# def example():
#    for i in range(100000000):
#        continue
#
#
# exampl()


# def my_decorator(func):
#    def wrapper():
#        print("Что-то перед вызовом")
#        func()
#        print("Что-то после вызова")
#
#    return wrapper
#
#
# @my_decorator
# def say_hello():
#    print("Hello!")
#
#
# say_hello()

#
import random

# def new_decorator(func):
#    def check():
#        result = func()
#        if isinstance(result, float):
#            return round(result)
#        else:
#            return result
#
#    return check
#
#
# @new_decorator
# def random_numbers():
#    return random.uniform(120, 456)
#
#
# say_hello = new_decorator(random_numbers)
#
# print(say_hello())


# def check_integers(func):
#    def wrapper(*args, **kwargs):
#        result = func(*args, **kwargs)
#        # Проверка на тип с использованием type()
#        if type(result) == float:
#            return round(result)
#        elif type(result) in (list, tuple):
#            rounded = [round(x) if type(x) == float else x for x in result]
#            # Возвращаем тот же тип, что и исходный (list или tuple)
#            return type(result)(rounded)
#        else:
#            return result
#
#    return wrapper


# elem = [1, 2, 3, [3, 2, 1], (1, 2, 3)]
# for i in elem:
#    print(type(i))


# ################################################################## Декоратор повторно вызывающий декорируемую
# функцию заданноне количество раз через заданное время, если произошла ошибка. Параметры, передаваемые в декоратор,
# обязательно именованные


# from functools import wraps
# import time
#
# def retry(*, retries=3, delay=3):
#    def wrapper(func):
#        @wraps(func)
#        def inner(*args, **kwargs):
#            for i in range(retries):
#                try:
#                    return func(*args, **kwargs)
#                except:
#                    time.sleep(delay)
#            raise Exception('Function call failed after multiple retries.')
#        return inner
#    return wrapper

# ################################################################## Декоратор который проверяет что все числа
# декорируемой функции являются целыми и округляет их до целых, если это не так
from functools import wraps, reduce

# def check_floats(precision):
#    def decorator(func):
#        @wraps(func)
#        def inner(*args, **kwargs):
#            result = func(*args, **kwargs)
#            # Проверка на тип с использованием type()
#            if type(result) == float:
#                return round(result, precision)
#            elif type(result) in (list, tuple):
#                rounded = [round(x, precision) if type(x) == float else x for x in result]
#                return type(result)(rounded)
#            else:
#                return result
#        return inner
#    return decorator

# Декоратор выполняющий повторные выполнения функции в случае ошибок
# def retry_decorator(max_retries):
#    def decorator(func):
#        def wrapper(*args, **kwargs):
#            for _ in range(max_retries):
#                try:
#                    result = func(*args, **kwargs)
#                    return result
#                except Exception as e:
#                    print(f"Retrying... ({e})")
#            raise Exception(f"Max retries exceeded")
#        return wrapper
#    return decorator
#

# from functools import wraps
# import pytest
#
#
# def ch_that_arg_is(predicate, error_message):
#    def wrapper(function):
#        @wraps(function)
#        def inner(arg):
#            if not predicate(arg):
#                raise ValueError(error_message)
#            return function(arg)
#
#        return inner
#
#    return wrapper
#
#
# def predicate_is_in(x):
#    return type(x) == int
#
#
# def predicate_is_positive(x):
#    return x > 0
#
#
# @ch_that_arg_is(predicate_is_in, "Значение должно быть целым числом")
# @ch_that_arg_is(predicate_is_positive, "Число должно быть положительным")
# def square(x):
#    """ Возведение числа в квадрат """
#    return x * x
#
#
# if __name__ == "__main__":
#    with pytest.raises(ValueError, match="Число должно быть положительным"):
#        square(-2)
#


# import time
#
# def benchmark(func):
#    def wrapper(*args, **kwargs):
#        t = time.time()
#        res = func(*args, **kwargs)
#        print(func.__name__, time.time()-t)
#        return res
#    return wrapper
#
#
# def logging(func):
#    def wrapper(*args, **kwargs):
#        res = func(*args, **kwargs)
#        print(func.__name__, args, kwargs)
#        return res
#    return wrapper
#
#
# def counter(func):
#    def wrapper(*args, **kwargs):
#        wrapper.count = wrapper.count + 1
#        res = func(*args, **kwargs)
#        print('{0} has been used: {1}x'.format(func.__name__, wrapper.count))
#        return res
#    wrapper.count = 0
#    return wrapper
#
# @counter
# @benchmark
# @logging
# def reverse_string(string):
#    return str(reversed(string))
#
# text = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.'
# print(reverse_string(text))
# print(reverse_string(text * 1000))


# import time
# t = time.time()
# while True:
#    print(round(time.time() - t), end="\t")
#    time.sleep(1)


# def positive_integers(func):
#    def wrapper(*args):
#        for arg in args:
#            if arg <= 0:
#                raise ValueError("All arguments must be positive integers")
#        return func(*args)
#    return wrapper
#
#
# @positive_integers
# def multiply(*args):
#    result = 1
#    for arg in args:
#        result *= arg
#    return result
#
#
# print(multiply(2, 3, 4))
# print(multiply(2, 0, 4))


# def is_palindrome(func):
#    def wrapper(text):
#        if text.lower() != text[::-1].lower():
#            raise ValueError("Argument must be a palindrome")
#        return func(text)
#    return wrapper
#
# @is_palindrome
# def reverse_string(string):
#    return string[::-1]
#
#
# print(reverse_string("racecar"))
# print(reverse_string("Racecar"))
# print(reverse_string("Hello"))


# def logging(func):
#    def wrapper(*args, **kwargs):
#        result = func(*args, **kwargs)
#        print(f"Function {func.__name__} called with args: {args} and kwargs: {kwargs}. Result: {result}")
#        return result
#    return wrapper
#
#
# @logging
# def multiply(x, y):
#    return x * y
#
# print(multiply(2, 3))

import time
#
#
#def slowit(n=1):
#    def decorator(func):
#        def wrapper(*args):
#            sleep(n)
#            return func(*args)
#
#        return wrapper
#
#    return decorator
#
#
#def timeit(func):
#    def wrapper(*args):
#        start_time = time()
#        result = func(*args)
#        end_time = time()
#        print(f"Time execution: {end_time - start_time}")
#        return result
#
#    return wrapper
#
#
#
#def memorize(func):
#    cashe = {}
#    def wrapper(*args):
#        if args in cashe:
#            return cashe[args]
#        result = func(*args)
#        cashe[args] = result
#        return result
#    return wrapper
#
## @memorize
#@timeit
#@memorize
#@slowit(2)
#def product(n):
#    return reduce(lambda x, y: x * y, range(1, n + 1)) if n > 0 else None
#
#print(product(10))

print(time.strftime("%H:%M:%S"))
