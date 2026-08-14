def calculate_total(price, tax):
    return price + tax

# Bug: tax is a string, which will crash when added to an integer
print(calculate_total(100, '0.05'))
def divide_numbers(a, b):
    # Potential bug: ZeroDivisionError
    return a / b

print(divide_numbers(10, 0))
