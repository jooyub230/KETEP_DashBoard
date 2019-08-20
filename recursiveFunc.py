
def recursFivo(num):
    if(num == 1):
        return 1
    elif (num > 1):
        return recursFivo(num-1)+recursFivo(num-2)
    else:
        return 0

for i in range(1, 10):
    print(recursFivo(i))
