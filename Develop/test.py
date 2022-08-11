from time import sleep
def cycle(arr):
    res = arr
    res.append(res[0])
    res.pop(0)
    return res

item = [".",".",".",".","O"]
while True:
    sleep(0.05)
    print(item)
    item = cycle(item)