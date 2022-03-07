import numpy as np
def loopover(mixed_up_board, solved_board):
    global solution
    solution = []
    #acutal gives arrays in format 'ABCD\nabcd'
    if '\n' in mixed_up_board:
        arr = mixed_up_board.split('\n')
        arr1 = solved_board.split('\n')
    else:
        arr = mixed_up_board
        arr1 = solved_board
    for i in range(len(arr)):
        arr[i] = list(arr[i])
    for i in range(len(arr1)):
        arr1[i] = list(arr1[i])
    arr = np.asarray(arr)
    fin = np.asarray(arr1)
    solution = run(arr,fin)
    #test gives in format ['abc','abc']
    if solution == None:
        return None
    return solution

def run(arr,fin):
    for i in range(len(arr)-1):
        for j in range(len(arr[0])):
            arr = row0(arr,fin,fin[i][j])
    for i in range(len(arr[0])-2):
        arr= row3(arr,fin,fin[len(arr)-1][i])
    if (arr==fin).all():
        return solution
    arr = algor(arr,3,[len(arr)-1,len(arr[0])-2],fin)
    if type(arr) == type(True):
        return None
    if (arr==fin).all():
        return solution
    return None
    
    
solution = []
def row0(arr,fin,index):
    loc2 = list(zip(*np.where(fin == index)))[0]
    loc1 = list(zip(*np.where(arr == index)))[0]
    if loc1 == loc2:
        return arr
    if loc1[0] == loc2[0]: #y cord is the same
        arr = move(arr,loc1[1],'d')
        arr = move(arr,loc1[0]+1,'l')
        arr = move(arr,loc1[1],'u')
        arr = row0(arr,fin,index)
    elif loc1[1] == loc2[1]: #x cord is the same
        arr = move(arr,loc1[0],'r')
        arr = row0(arr,fin,index)
    elif loc1[0] > loc2[0]: #unsolved y > solved y
        #move row (solved row) to unsolved location
        for i in range(loc1[0] - loc2[0]):
            arr = move(arr,loc2[1],'d')
        if loc1[1]-loc2[1] >0:
            for i in range(loc1[1] - loc2[1]): #maybe issue is negative values
                arr = move(arr,loc1[0],'l')
        else:
            for i in range(loc2[1] - loc1[1]):
                arr = move(arr,loc1[0],'r')
        for i in range(loc1[0]-loc2[0]):
            arr = move(arr,loc2[1],'u')
        arr = row0(arr,fin,index)
    return arr

def row2(arr,fin,index):
    loc2 = list(zip(*np.where(fin == index)))[0]
    loc1 = list(zip(*np.where(arr == index)))[0]
    for i in range(loc1[1] - loc2[1]):
        arr = move(arr,loc1[0],'l')
    return arr
def row3(arr,fin,index):
        #123 -> 231 
        #123 -> 312
    #[u,v,w,x,y]
    #case [u,w,x,y,v]
    #where is V
    loc1 = list(zip(*np.where(arr == index)))[0]
    loc2 = list(zip(*np.where(fin == index)))[0]
    if loc2 == loc1:
        return arr
    elif loc1[1] -loc2[1] >=3:
        print('case1 algo2 on loc-1')
        arr = algor(arr,2,[loc1[0],loc1[1]-1])
        arr = row3(arr,fin,index)
        #run algor 2 on 3 where 3rd is V, loc1-2,loc1-1,loc1
        #rerun
    elif loc1[1] - loc2[1] == 2:
        print('case2 algo2 on loc-1')
        arr = algor(arr,2,[loc1[0],loc1[1]-1])
        arr = row3(arr,fin,index)
        #run algor 2 on loc1, loc1-2,loc1-1,loc1
        #rerun
    elif loc1[1] - loc2[1] == 1:
        print('case3 algo1 on loc')
        arr = algor(arr,1,[loc1[0],loc1[1]])
        arr = row3(arr,fin,index)
    return arr

def algor(arr,num,loc2,fin=[]):
    if num == 1:
        #123 -> 231 
        #123 -> 312
        for i in 'dlurdlurrdllur':
            if i in 'lr':
                arr = move(arr,loc2[0],i)
            elif i in 'ud':
                arr = move(arr,loc2[1],i)
    if num == 2:
        for i in 'ldruldrurdlu':
            if i in 'lr':
                arr = move(arr,loc2[0],i)
            elif i in 'ud':
                arr = move(arr,loc2[1],i)
    if num == 3:
        ploc1 = [len(arr)-1,len(arr[0])-1]
        ploc2 = [len(arr)-1,len(arr[0])-2]
        for i in 'urul'*11: # for 4x4 urulurulu
            #    'urulurulurul 
            if i in 'lr':
                arr = move(arr,len(arr)-1,i)
            elif i in 'ud':
                arr = move(arr,len(arr[0])-1,i)
            if arr[ploc1[0]][ploc1[1]] == fin[len(arr)-1][len(arr[0])-1]:
                if arr[ploc2[0]][ploc2[1]] == fin[len(arr)-1][len(arr[0])-2]:
                    #positions have swapped
                    break
            if arr[ploc1[0]][ploc1[1]] == fin[len(arr)-1][len(arr[0])-2]:
                if arr[ploc2[0]][ploc2[1]] == fin[len(arr)-1][len(arr[0])-1]:
                    #did full loop, go to parity option
                    arr = parityfix(arr,fin)
                    break 

##            parityfix = '''
##do ldlu until L and Q are swapped
##r
##do ldlu until Q and R are swapped
##l
##do ldlu undil Q and L are swapped
##
##'''
    return arr
def parityfix(arr,fin):
    ploc1 = [len(arr)-1,len(arr[0])-1]
    ploc2 = [len(arr)-1,len(arr[0])-2]
    ploc3 = [len(arr)-2,len(arr[0])-1]
    #ploc1 = bottom right of arr
    #ploc2 = bottom right-1 of arr
    yn = 0
    while yn == 0:
        for i in 'ldlu':
            if i in 'lr':
                arr = move(arr,len(arr)-1,i)
            elif i in 'ud':
                arr = move(arr,len(arr[0])-1,i)
            if arr[ploc1[0]][ploc1[1]] == fin[len(arr)-1][len(arr[0])-2]:
                if arr[ploc2[0]][ploc2[1]] == fin[len(arr)-1][len(arr[0])-1]:    
                    #did full loop
                    yn = -1
                    break
            elif arr[ploc1[0]][ploc1[1]] == fin[len(arr)-2][len(arr[0])-1]:
                if arr[ploc3[0]][ploc3[1]] == fin[len(arr)-1][len(arr[0])-2]:    
                    #positions have swapped
                    yn = 1
                    break
    if yn == -1:
        return True
    arr = move(arr,len(arr)-1,'r')
    count = 0
    while yn == 1:
        for i in 'ldlu':
            count+=1
            if i in 'lr':
                arr = move(arr,len(arr)-1,i)
            elif i in 'ud':
                arr = move(arr,len(arr[0])-1,i)
            if arr[ploc1[0]][ploc1[1]] == fin[len(arr)-2][len(arr[0])-1]:
                if arr[ploc3[0]][ploc3[1]] == fin[len(arr)-1][len(arr[0])-2]:
                    if count !=1:
                        #did full loop
                        yn = -1
                        break
            elif arr[ploc1[0]][ploc1[1]] == fin[len(arr)-1][len(arr[0])-2]:
                if arr[ploc3[0]][ploc3[1]] == fin[len(arr)-1][len(arr[0])-1]:    
                    #positions have swapped
                    yn = 2
                    break
    if yn == -1:
        return True
    arr = move(arr,len(arr)-1,'l')
    while yn == 2:
        for i in 'ldlu':
            if i in 'lr':
                arr = move(arr,len(arr)-1,i)
            elif i in 'ud':
                arr = move(arr,len(arr[0])-1,i)
            if arr[ploc1[0]][ploc1[1]] == fin[len(arr)-1][len(arr[0])-2]:
                if arr[ploc3[0]][ploc3[1]] == fin[len(arr)-1][len(arr[0])-1]:     
                    #did full loop
                    yn = -1
                    break
            elif arr[ploc1[0]][ploc1[1]] == fin[len(arr)-1][len(arr[0])-1]:
                if arr[ploc2[0]][ploc2[1]] == fin[len(arr)-1][len(arr[0])-2]:    
                    #positions have swapped
                    yn = 3
                    break
    if yn == -1:
        return True
    return arr
        
        
    
            
def move(arr,pos,direction):
    global solution
    if direction == 'l':
        arr[pos] = np.roll(arr[pos],-1)
    elif direction == 'r':
        arr[pos] = np.roll(arr[pos],1)
    elif direction == 'u':
        arr[:,pos] = np.roll(arr[:,pos],-1)
    elif direction == 'd':
        arr[:,pos] = np.roll(arr[:,pos],1) 
    solution.append(direction.upper()+str(pos))
    return arr
