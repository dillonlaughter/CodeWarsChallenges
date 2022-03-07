notes = '''
get everything but the bottom 2 rows in the correct position
math for bottom 2 rows

'''
import numpy as np
def slide_puzzle(ar):
    global solution
    solution = []
    sol = []
    arr,fg = basics(ar)
    sol = asdf(arr,fg)
    sol = np.asarray(sol)
    if type(sol) == type(np.asarray([])):
        if len(sol) ==0:
            return None
        return sol.tolist()
    return None#[6,7,11,12]


def move(arr,direction,adder=0):#direction or number?
    global solution
    loc0 = list(zip(*np.where(arr==0)))
    if direction == 'l':
        if adder==0:solution.append(arr[loc0[0][0]][loc0[0][1]-1])
        arr[loc0[0][0]][loc0[0][1]],arr[loc0[0][0]][loc0[0][1]-1]= arr[loc0[0][0]][loc0[0][1]-1],arr[loc0[0][0]][loc0[0][1]]
    if direction == 'r':
        if adder ==0:solution.append(arr[loc0[0][0]][loc0[0][1]+1])
        arr[loc0[0][0]][loc0[0][1]],arr[loc0[0][0]][loc0[0][1]+1]= arr[loc0[0][0]][loc0[0][1]+1],arr[loc0[0][0]][loc0[0][1]]
    if direction == 'u':
        if adder==0:solution.append(arr[loc0[0][0]-1][loc0[0][1]])
        arr[loc0[0][0]][loc0[0][1]],arr[loc0[0][0]-1][loc0[0][1]]= arr[loc0[0][0]-1][loc0[0][1]],arr[loc0[0][0]][loc0[0][1]]
    if direction == 'd':
        if adder==0:solution.append(arr[loc0[0][0]+1][loc0[0][1]])
        arr[loc0[0][0]][loc0[0][1]],arr[loc0[0][0]+1][loc0[0][1]]= arr[loc0[0][0]+1][loc0[0][1]],arr[loc0[0][0]][loc0[0][1]]
    return arr
def basics(arr__arr_fg):
    arr = arr__arr_fg
    fg=np.arange(1,len(arr)*len(arr[0])+1).reshape(len(arr[0]),len(arr))
    fg[-1][-1] = 0
    arr = np.asarray(arr)
    arr =movetobase(arr)
    return arr,fg

#after each index, return the 0 to the bottom right
def row1_0(arr,index,fg):#?
    
    loc = list(zip(*np.where(arr == index)))
    floc = list(zip(*np.where(fg == index)))
    if loc != floc:
        #if 0 on base location
        if loc[0][0] == list(zip(*np.where(arr==0)))[0][0]:#index loc same y as 0
            arr = move(arr,'u')
            while list(zip(*np.where(arr == 0)))[0][1] != loc[0][1]:
                arr = move(arr,'l')
            arr = move(arr,'d')
            arr = movetobase(arr)
            arr = row1_0(arr,index,fg)
        elif loc[0][1] ==list(zip(*np.where(arr==0)))[0][1]:#index loc same x as 0
            arr = move(arr,'l')
            while list(zip(*np.where(arr == 0)))[0][0] != loc[0][0]:
                arr = move(arr,'u')
            arr = move(arr,'r')
            arr = movetobase(arr)
            arr = row1_0(arr,index,fg)
        elif floc[0][0] == loc[0][0]: #final y == index y
            while list(zip(*np.where(arr == 0)))[0][0] != loc[0][0]+1:
                arr = move(arr,'u')
            while list(zip(*np.where(arr == 0)))[0][1] != loc[0][1]:
                arr = move(arr,'l')
            while floc != list(zip(*np.where(arr == index))):
                arr = mover(arr,'lurdl')
        elif floc[0][1] == loc[0][1]: #final x == index x
            while list(zip(*np.where(arr == 0)))[0][0] != loc[0][0]:
                arr = move(arr,'u')
            while list(zip(*np.where(arr == 0)))[0][1] != loc[0][1]+1:
                arr = move(arr,'l')
            while floc != list(zip(*np.where(arr == index))):
                arr = mover(arr,'uldru')
        else:
            while list(zip(*np.where(arr == 0)))[0][0] != loc[0][0]:
                arr = move(arr,'u')
            while list(zip(*np.where(arr == 0)))[0][1] != loc[0][1]+1:
                arr = move(arr,'l')
            while list(zip(*np.where(arr == index)))[0][0] != floc[0][0]+1:
                arr = mover(arr,'uldru')
            while floc[0][1] > list(zip(*np.where(arr == index)))[0][1]:
                arr = mover(arr,'ldrru')
            while floc[0][1] < list(zip(*np.where(arr == index)))[0][1]:
                arr = mover(arr,'dllur')
            arr = mover(arr,'uld')
            arr =movetobase(arr)
            arr = row1_0(arr,index,fg)
            
    arr = movetobase(arr)
    return arr
def row1_1(arr,index,fg):
    loc = list(zip(*np.where(arr == index)))
    floc = list(zip(*np.where(fg == index)))
    if loc != floc:
        if loc[0][0] == list(zip(*np.where(arr==0)))[0][0]:#index loc same y as 0
            arr = move(arr,'u')
            while list(zip(*np.where(arr == 0)))[0][1] != loc[0][1]:
                arr = move(arr,'l')
            arr = move(arr,'d')
            arr = movetobase(arr)
            arr = row1_1(arr,index,fg)
        elif loc[0][1] ==list(zip(*np.where(arr==0)))[0][1]:#index loc same x as 0
            arr = move(arr,'l')
            while list(zip(*np.where(arr == 0)))[0][0] != loc[0][0]:
                arr = move(arr,'u')
            arr = move(arr,'r')
            arr = movetobase(arr)
            arr = row1_1(arr,index,fg)
        else:
            while loc[0][0] != list(zip(*np.where(arr==0)))[0][0]:
                arr = move(arr,'u')
            while loc[0][1]+1 != list(zip(*np.where(arr==0)))[0][1]:
                arr = move(arr,'l')
            while list(zip(*np.where(fg == index-1)))[0][1] != list(zip(*np.where(arr==index)))[0][1]:#maybe error here
                arr = mover(arr,'ldrru')
            while list(zip(*np.where(fg == index-1)))[0][0]+1 != list(zip(*np.where(arr == index)))[0][0]:
                arr = mover(arr,'uldru')
            arr = mover(arr,'ldruuldrdluurd')
    arr = movetobase(arr)
    return arr
    
def mover(arr,string):
    for i in string:
        arr = move(arr,i)
    return arr
def asdf(arr,fg):
    for i in range(len(arr)-2):
        for j in range(len(arr[0])-1):
            #on 5x5 grid, run first 4 elements on first 3 rows
            arr = row1_0(arr,fg[i][j],fg)
        #on 5x5 grid, run last element on first 3 rows
        arr = row1_1(arr,fg[i][j+1],fg)
    for i in range(len(arr[0])-2):
        #on 5x5 grid, run first 3 columns on bottom 2 rows
        arr = row2_0(arr,i,fg)
    for i in range(4):
        #alternate positions of remaining 2x2 grid in bottom right
        arr = row2_1(arr,fg)
        if (arr == fg).all():
            #return solution if it matches the expected
            return solution
    return []
    

def row2_1(arr,fg):
    arr = mover(arr,'lurd')
    return arr

def row2_0(arr,index,fg):
    num1 = fg[len(arr)-2][index]
    num2 = fg[len(arr)-1][index]
    loc1 = list(zip(*np.where(arr == num1)))
    loc2 = list(zip(*np.where(arr == num2)))
    #################GET BOTH OFF OF RIGHT WALL,redo loc1,loc2
    while loc1[0][1] == list(zip(*np.where(arr==0)))[0][1] or loc2[0][1] == list(zip(*np.where(arr==0)))[0][1]:        
        arr =mover(arr,'l'*(len(arr[0])-index-1))
        arr = move(arr,'u')
        arr =movetobase(arr)
        loc1 = list(zip(*np.where(arr == num1)))
        loc2 = list(zip(*np.where(arr == num2)))
    loc1 = list(zip(*np.where(arr == num1)))
    loc2 = list(zip(*np.where(arr == num2)))
    part1 = loc1[0][1]+1 == loc2[0][1] and loc2[0][0] == loc1[0][0]
    part2 = loc1[0][1]-1 == loc2[0][1] and loc2[0][0] == loc1[0][0]
    if not(part1 or part2):#if the 2 elements looking at arent beside each other
        #if num2 x > num1 x
        if loc2[0][1] > loc1[0][1]:
            #if num2 is top row
            if loc2[0][0] == len(arr)-2:
                #if num1 is top row
                if loc1[0][0] == len(arr)-2:
                    while list(zip(*np.where(arr==num2)))[0][1] != list(zip(*np.where(arr==0)))[0][1]:
                        arr = move(arr,'l')
                    while list(zip(*np.where(arr==num1)))[0][1]+1 != list(zip(*np.where(arr==num2)))[0][1]:
                        arr = mover(arr,'lurdl')
                    arr = movetobase(arr)
                    arr = row2_0(arr,index,fg)
                #if num1 is bottom row
                elif loc1[0][0] == len(arr)-1:
                    while list(zip(*np.where(arr==0)))[0][1] != loc2[0][1]:
                        arr=move(arr,'l')
                    arr = move(arr,'u')
                    while list(zip(*np.where(arr==num1)))[0][1]+1 != list(zip(*np.where(arr==num2)))[0][1]:
                        arr= mover(arr,'ldrul')
                    arr = movetobase(arr)
                    arr = row2_0(arr,index,fg)
                        
            #if num2 is bottom row
            elif loc2[0][0] == len(arr)-1:
                #if num1 is top row
                if loc1[0][0] == len(arr)-2:
                    arr = move(arr,'u')
                    while list(zip(*np.where(arr==0)))[0][1] != loc2[0][1]:
                        arr = move(arr,'l')
                    arr = move(arr,'d')
                    while list(zip(*np.where(arr==num1)))[0][1]+1 != list(zip(*np.where(arr==num2)))[0][1]:
                        arr = mover(arr,'lurdl')
                    arr = movetobase(arr)
                    arr = row2_0(arr,index,fg)
                    
                #if num1 is bottom row
                elif loc1[0][0] == len(arr)-1:
                    arr = move(arr,'u')
                    while list(zip(*np.where(arr==0)))[0][1] != loc2[0][1]:
                        arr = move(arr,'l')
                    while list(zip(*np.where(arr==num1)))[0][1]+1 != list(zip(*np.where(arr==num2)))[0][1]:
                        arr = mover(arr,'ldrul')
                    arr = movetobase(arr)
                    arr = row2_0(arr,index,fg)
                    
        #if num2 x < num1 x
        else:
            if loc2[0][1] < loc1[0][1]:
                #if num2 is top row
                if loc2[0][0] == len(arr)-2:
                    #if num1 is top row
                    if loc1[0][0] == len(arr)-2:
                        while list(zip(*np.where(arr==0)))[0][1] != loc1[0][1]:
                            arr = move(arr,'l')
                        while list(zip(*np.where(arr==num1)))[0][1]-1 != list(zip(*np.where(arr==num2)))[0][1]:
                            arr = mover(arr,'lurdl')
                        arr = movetobase(arr)
                        arr = row2_0(arr,index,fg)
                    #if num1 is bottom row
                    elif loc1[0][0] == len(arr)-1:
                        arr = move(arr,'u')
                        while list(zip(*np.where(arr==0)))[0][1] != loc1[0][1]:
                            arr = move(arr,'l')
                        arr = move(arr,'d')
                        while list(zip(*np.where(arr==num1)))[0][1]-1 != list(zip(*np.where(arr==num2)))[0][1]:
                            arr = mover(arr,'lurdl')
                        arr = movetobase(arr)
                        arr = row2_0(arr,index,fg)
                        
                #if num2 is bottom row
                elif loc2[0][0] == len(arr)-1:
                    #if num1 is top row
                    if loc1[0][0] == len(arr)-2:
                        while list(zip(*np.where(arr==0)))[0][1] != loc1[0][1]:
                            arr = move(arr,'l')
                        arr = move(arr,'u')
                        while list(zip(*np.where(arr==num1)))[0][1]-1 != list(zip(*np.where(arr==num2)))[0][1]:
                            arr = mover(arr,'ldrul')
                        arr = movetobase(arr)
                        arr = row2_0(arr,index,fg)
                        
                    #if num1 is bottom row
                    elif loc1[0][0] == len(arr)-1:
                        arr = move(arr,'u')
                        while list(zip(*np.where(arr==0)))[0][1] != loc1[0][1]:
                            arr = move(arr,'l')
                        while list(zip(*np.where(arr==num1)))[0][1]-1 != list(zip(*np.where(arr==num2)))[0][1]:
                            arr = mover(arr,'ldrul')
                        arr = movetobase(arr)
                        arr = row2_0(arr,index,fg)
                    
        #if num2 is same x as num1
            else:
                if loc2[0][1] == loc1[0][1]:
                    while list(zip(*np.where(arr==0)))[0][1] != loc1[0][1]+1:
                        arr = move(arr,'l')
                    arr = mover(arr,'lu')
                    arr = movetobase(arr)
                    arr = row2_0(arr,index,fg)
            
    else:#they are beside each other in some way lr or rl
        #loc2 x > loc1x        
        if loc2[0][1] > loc1[0][1]:
            #both in top row
            if loc1[0][0] == len(arr)-2:
                while list(zip(*np.where(arr==0)))[0][1] != loc2[0][1]:
                    arr = move(arr,'l')
                arr = mover(arr,'urdluldrurdlurdl')#[...21,16...],[...0,x,...]
                while list(zip(*np.where(arr==num2)))[0][1] - index != 0:
                    arr = mover(arr,'lurrdll')
                arr = mover(arr,'ur')
                arr = movetobase(arr)
            #else
            else:
                arr= move(arr,'u')
                while list(zip(*np.where(arr==0)))[0][1] != loc1[0][1]:
                    arr = move(arr,'l')
                while list(zip(*np.where(arr==num1)))[0][1] - index != 0:
                    arr = mover(arr,'ldrrull')
                arr = mover(arr,'dr')
                arr = movetobase(arr)
        #if loc2 x < loc1x
        elif loc2[0][1] < loc1[0][1]:
            if loc1[0][0] == len(arr)-2:
                while list(zip(*np.where(arr==0)))[0][1] != loc2[0][1]:
                    arr = move(arr,'l')
                while list(zip(*np.where(arr==num2)))[0][1] - index != 0:
                    arr = mover(arr,'lurrdll')
                arr = mover(arr,'ur')
                arr = movetobase(arr)
            #else
            else:
                arr= move(arr,'u')
                while list(zip(*np.where(arr==0)))[0][1] != loc1[0][1]:
                    arr = move(arr,'l')
                arr = mover(arr,'druldlurdruldrul')#[...21,16...],[...0,x,...]
                while list(zip(*np.where(arr==num1)))[0][1] - index != 0:
                    arr = mover(arr,'ldrrull')
                arr = mover(arr,'dr')
                arr = movetobase(arr)
    return arr
        
        
def movetobase(arr): #reset the 0 back to bottom right for ease
    while list(zip(*np.where(arr==0)))[0][1] != len(arr[0])-1:
        arr = move(arr,'r')
    while list(zip(*np.where(arr==0)))[0][0] != len(arr)-1:
        arr = move(arr,'d')
    return arr
