from sre_parse import ASSERT

import pytest

# from _typeshed import SupportsRichComparison
from simple_calculator import (
    Calculate,
    CalculatorState,
    HandleKeyPress,
    Parse,
)


def test_parse():
    assert Parse("") == []  # Empty input => empty list
    assert Parse("    ") == []  # Whitespace input => empty list
    assert Parse("  1  +  2  =  ") == [
        "1",
        "+",
        "2",
        "=",
    ]  # Testing parsing with extra spaces


def test_handle_key_press():
    # Testing single digit key
    state = CalculatorState()
    HandleKeyPress(state, "9")
    assert state.screen == 9

    # Testing empty input (space key)
    state = CalculatorState()
    HandleKeyPress(state, " ")
    assert state.screen == 0

    # Testing beginning from zeros (03 => 3)
    state = CalculatorState()
    HandleKeyPress(state, "0")
    HandleKeyPress(state, "3")
    assert state.screen == 3

    # Testing operations key
    state = CalculatorState()
    HandleKeyPress(state, "7")
    HandleKeyPress(state, "*")
    assert state.first_number == 7
    assert state.op == "*"
    assert state.start_second_number
    assert state.screen == 7

    # Test first anf second number
    state = CalculatorState()
    HandleKeyPress(state, "1")
    HandleKeyPress(state, "5")
    HandleKeyPress(state, "+")
    HandleKeyPress(state, "2")
    HandleKeyPress(state, "6")
    # HandleKeyPress(state, "=")
    assert state.first_number == 15
    assert state.screen == 26


def test_calculate(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda *args: "1 + 1 = \n")
    assert Calculate(Parse(input().strip())) == 2

    # Test empty input
    assert Calculate([]) == 0

    # Test not full statement
    assert Calculate(["1", "+", "2"]) == 2

    # Test invalid input
    assert Calculate(["1", "+", "a", "="]) == 0

    # Test invalid input with missing =
    assert Calculate(["1", "+", "2", "+"]) == 2

    # Test addition
    assert Calculate(["9", "9", "9", "+", "1", "="]) == 1000

    # Test subsctraction
    assert Calculate(["6", "7", "8", "-", "78", "="]) == 600

    # Test multiplication
    assert Calculate(["1", "5", "*", "5", "="]) == 75

    # Test division
    assert Calculate(["1", "0", "/", "2", "="]) == 5

    # Test division returns int
    assert isinstance(Calculate(["5", "/", "5", "="]), int)

    # Test division by zero
    assert Calculate(["1", "0", "/", "0", "="]) == 0

    # Test result of division is rounded down
    assert Calculate(["1", "0", "/", "3", "="]) == 3
    assert Calculate(["1", "0", "/", "4", "="]) == 2
