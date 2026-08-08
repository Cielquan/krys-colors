#!/usr/bin/env python3
"""File docstring."""
import asyncio
from logging import *
import logging
from typing import List as List
import typing as t


def decorator_ohne_param() -> None:
    pass


@decorator_ohne_param
def decorator(param: str) -> str:
    """Decorator returning given parameter string.

    >>> print('''hello
    ... world''')

    :param param: String to return
    :return: Given string
    """
    return param


@decorator(param="string")
def numbers(num: int = 32) -> None:
    x = - num + 0xdeadbeef - 0b00100001 * 0o0123 / 1.0 // 1_005_123 ** .10e12 % 2j
    x += 1
    x = ~ 1 << 2 >> 3 & 4 | 5 ^ 6
    x = [1, 2] @ [1, 2]
    x = 0123  # Numbers with leading zeros are invalid in Python 3


def strings() -> str:
    """Docstring."""
    strings: str = \
    'single quoted'[0:-1] \
    + "double quoted".upper() \
    + '''single quoted multiline''' \
    + """double quoted multiline""" \
    + u"string" \
    + "Cyrillic Я is \u042f. Invalid escape: \u042g" \
    + R"Raw string \n ignoring escapes." \
    + r"^Regex string [^1-9]$"

    byte: bytes = b"newline: \n and newline as byte: \x0a"

    f_string = f"Here comes the formatted part: {strings!s:{'^10'}}"
    format_string = "{0:^10} {} {key!r}".format(byte, f_string, key=f_string)
    print(percent_string:="%-5.10s %d" % (format_string, numbers()))
    return percent_string


def collection_types() -> None:
    {"key": "value", 1: 2}
    {"only", "unique", "stay", 1 , 2}
    ["some", "amount", "of", "items", 1, 2]
    ("fixed", "length", "list", 1 , 2)


def loops() -> None:
    while 1 not in [] and True is not False or 1 < 2 > 1 != 2 == 2 >= 2 <= 3:
        break

    for idx, i in enumerate((1, 2)):
        breakpoint()
        assert idx > 0
        print(i)
        continue


def pattern_matching() -> None:
    match "foo":
        case 1 | 2:
            print("1/2")
        case "foo":
            print("foo")
        case _:
            print("catch all")


def exc_handling() -> None:
    try:
        raise ValueError("error")
    except ValueError as exc:
        print(exc)
    finally:
        pass


class AsyncCounter:
    def __init__(self, limit):
        self.current = 0
        self.limit = limit

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.current >= self.limit:
            raise StopAsyncIteration

        await asyncio.sleep(0.5)

        value = self.current
        self.current += 1
        return value


async def async_main(
    _foo: None,
) -> None:
    async with asyncio.Lock():
        await asyncio.sleep(0)

    async for i in AsyncCounter(1):
        print(i)


class Bar():

    def __init__(self):  # type: ignore
        array1: List[str] = []
        array2 = []  # type: List[T]  # PEP 484
        return array1 + array2

    @classmethod
    def create(cls) -> "Bar":
        return cls()


class Foo(Bar):

    class_var: str

    def __init__(self, param: str) -> None:
        """Init docstring."""
        super().__init__()
        self.param = param

    def call_init(self) -> None:
        self.__init__(param=self.__init__.__doc__)


lambda_adding = lambda x, y: x + y


def generic_swap[T, U](a: T, b: U) -> tuple[U, T]:
    return (b, a)


class Container[T]:
    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value

    def mapping[U: str | bytes](self, func: t.Callable[[T], U]) -> "Container[U]":
        return Container(func(self.value))
