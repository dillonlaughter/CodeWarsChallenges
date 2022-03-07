def find_position(num):
    num = str(num)
    search_list = []
    
    for step in range(len(num)+1):
        for start in range(step):
            search_query = parse(num, start, step)
            if search_query >= 0:
                search_list.append(search_query)

    if not len(search_list):
        return int(length_of(int('1' + num)) + 1)

    return int(min(search_list))


def parse(num, start, step):
    if start + step <= len(num):
        n = int(num[start:(start+step)])
    else:
        p1 = num[start:]
        p2 = num[0:start]
        var = len(p1) + len(p2) - step

        var1 = p2[var:]
        if var1 == '9' * len(var1):
            p1 += '0' * len(var1)
            n = int(p1)
        else:
            p1 = p1 + p2[var:]
            n = int(p1) + 1
        if str(n - 1)[(step - len(p2)):] != p2:
            return -1

    arr = []
    len1 = 0

    if start:
        prev = str(n - 1)
        arr.append(prev[(len(prev) - start):])
        len1 += start

    x = n
    while len1 < len(num):
        stra = str(x)
        if len(stra) + len1 > len(num):
            arr.append(stra[0:(len(num) - len1)])
            len1 += len(num) - len1
        else:
            arr.append(stra)
            len1 += len(stra)
        x += 1

    if ''.join(arr) == num:
        total = length_of(n)
        return total - start
    else:
        return -1
def length_of(n):
    total = 0
    len1 = 1
    x = 10
    while n > x:
        total += len1 * (x - x / 10)
        x *= 10
        len1 += 1
    total += len1 * (n - x / 10)
    return total
