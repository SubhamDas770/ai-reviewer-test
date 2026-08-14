def calculate_total(price, tax):
    return price + tax

# Bug: tax is a string, which will crash when added to an integer
print(calculate_total(100, '0.05'))
a=15
b=16
c= a+b
print(c)
