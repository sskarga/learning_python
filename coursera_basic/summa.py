# Сумма цифр в строке

import sys

digit_string = sys.argv[1]
sum = None

if ( len(digit_string) > 0 ) and digit_string.isdigit():
    sum = 0
    for char in digit_string:
        sum += int(char)
else:
    print("No digital!")

print(f"Сумма цифр в строке = {sum}")