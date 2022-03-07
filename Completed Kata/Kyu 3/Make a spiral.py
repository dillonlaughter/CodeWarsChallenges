def spiralize(size): #possibly make it a class file
    spiral = [[0 for i in range(int(size))] for j in range(int(size))]
    startleft = 0
    starttop = 0
    quanleft = int(size)
    quantop = int(size)
    if int(size)%2 == 0:
        q1 = int(size)
    else:
        q1 = int(size)+1
    for q in range(q1):
        quadrant = (q%4)+1
        if quadrant ==1:#in [1+4*x for x in range(10)]: #go left #done
            #startleft -= 2
            for i in range(quanleft-(2*((q)//4))): #7 ~ 3 #q+1?
                spiral[starttop][i+startleft-1] = 1
            #startleft += 2
        if quadrant ==2:#in [2+4*x for x in range(10)]: #go down # #7 ~ 3 #done
            for i in range(quantop): # (quantop - 2*??) || (quantop - ??)
                spiral[i+starttop][starttop + quantop - 1] = 1
        if quadrant ==3:#in [3+4*x for x in range(10)]: #go right #done
            for i in range(quanleft - starttop):#, startleft - 1,-1):
                spiral[int(size) - starttop - 1][i+starttop] = 1
        if quadrant ==4:#in [4+4*x for x in range(10)]: #go up
            for i in range(quantop - 2):#, y1 - 1,-1):
                spiral[i+starttop + 2][startleft] = 1
            startleft +=2
            quantop -= 4
            quanleft -=2
            starttop += 2

    return spiral
