def triangle(row):
    rgb = {'R':0, 'G':1, 'B':2}
    RGB = "RGB"
    num = len(row)
    x, y = 1, 0
    result = rgb[row[0]]
    for i in range(1, num):
        xx, yy = regen(num - i)
        y += yy
        x = x * xx % 3
        xx, yy = regen(i)
        y -= yy
        x = x * xx % 3
        if y == 0:
            result += rgb[row[i]] * x
    result %= 3
    if num % 2 == 0:
        result = (3 - result) % 3
    return RGB[result]

def regen(num):
    rem = 0
    while num % 3 == 0:
        num /= 3
        rem += 1
    return int(num % 3), rem
