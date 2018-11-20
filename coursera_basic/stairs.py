# Рисуем лестницу

import sys
num_steps = int(sys.argv[1])

for num in range(1, num_steps + 1):
    space = num_steps + 1 - num
    print(' ' * space + '#' * num)