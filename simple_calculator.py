class CalculatorState:
    # Function which represents state of calculator
    def __init__(self):
        self.screen = 0  # Current number displayed on screen
        self.first_number = 0  # First operand
        self.op = None  # Current operation (+,-,*,/)
        self.start_second_number = False  # Flag to start entering second number


def Parse(input_string):
    # Get the input string and divide into numbers and operators by spaces
    if not input_string or input_string.strip() == "":
        return []
    return input_string.strip().split()


def HandleKeyPress(state, key):
    # Handling the single key and updating calculators state

    if key in "0123456789":
        digit = int(key)
        if state.start_second_number:
            # Second number on screen starts
            state.screen = digit
            state.start_second_number = False
        else:
            # Appending digit to existing number
            state.screen = state.screen * 10 + digit

    elif key in "+-*/":
        state.first_number = state.screen
        state.op = key
        state.start_second_number = True

    elif key == "=":
        if state.op is not None:
            # Performing the operations
            if state.op == "+":
                state.screen = state.first_number + state.screen
            elif state.op == "-":
                state.screen = state.first_number - state.screen
            elif state.op == "*":
                state.screen = state.first_number * state.screen
            elif state.op == "/":
                state.screen = int(state.first_number / state.screen)
            # Reset operation state
            state.op = None
            state.start_second_number = False
    # else:
    # state.screen = state.first_number


def Calculate(keys):
    # Getting the list of strings keys (numbers/operators), calculating, returning result
    state = CalculatorState()

    for key in keys:
        HandleKeyPress(state, key)

    return state.screen


def main():
    input_string = input().strip()
    keys = Parse(input_string)
    result = Calculate(keys)
    print(result)


if __name__ == "__main__":
    main()
