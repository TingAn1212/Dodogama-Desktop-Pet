def cycle(arr):
    res = []
    last = None
    first = True
    for item in arr:
        if first:
            first = False
            last = item
        else:
            res.append(item)
    res.append(last)
    return res

print(cycle([1,2,3]))