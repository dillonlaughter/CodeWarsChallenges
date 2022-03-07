def validateBattlefield(field):
    'Setup'
    global test
    global res
    res = True
    test = [0,4,3,2,1]
    
    'Made Border of Zeroes'
    var = list('0'*(len(field)-2))
    for i in range(0,len(var)):
        var[i] = int(var[i])
    field.insert(0,var)
    field.insert(len(field),var)
    for i in range(0,len(field)):
        field[i].insert(0,0)
        field[i].insert(len(field[i])-1,0)
    
    'Find a "1"'
    for i in range(0,len(field)):
        for j in range(0,len(field[i])):
            if field[i][j] == 1:
                path_length = 1
                field[i][j] = 0
                find(field,i,j,path_length)
    if all(i == 0 for i in test):
        return True
    else:
        return False

'''Use found "1" and look around it,
    deleting new ones found and adding
    it to path_len'''
def find(field,i,j,path_len):
    bad = field[i-1][j]+field[i-1][j+1]+field[i][j+1]+field[i+1][j+1]+field[i+1][j]+field[i+1][j-1]+field[i][j-1]+field[i-1][j-1]
    if bad > 1:
        test[0] = -1
    elif field[i+1][j] == 1:
        path_len += 1
        field[i+1][j]=0
        find(field,i+1,j,path_len)
    elif field[i][j+1] == 1:
        path_len += 1
        field[i][j+1]=0
        find(field,i,j+1,path_len)
    else:
        field[i][j] = 0
        try:
            test[path_len] = test[path_len]-1
        except:
            test[0] = -1
