global debug
from copy import deepcopy
def train_crash(track,trainA,trainAstart,trainB,trainBstart,limit):
    print('qw '+"['''"+track.replace('\\',']')+"''','"+trainA+"',"+str(trainAstart)+",'"+trainB+"',"+str(trainBstart)+','+str(limit)+']')
    trainA,trainB = train(trainA,trainB)
    new,cross,old,crossS = setup(track,trainA,trainAstart,trainB,trainBstart)
    count,crashed = move(new,cross,limit,trainA,trainB,old,crossS)
    if crashed >0:
        if count <2:
            if count == -2:
                return 1
            return 0
        return count
    return -1


def move(new,cross,limit,tA,tB,old,crossS):
    global debug
    d2 = {}#{'e':[12,213],'f':[13,17]}
    print(cross)
    print(crossS)
    d3 = {}
    for i in cross:
        d2[cross[i]] = [old.index(cross[i]),old.index(cross[i],1+old.index(cross[i]))]
    for i in crossS:
        d3[crossS[i]] = [old.index(crossS[i]),old.index(crossS[i],1+old.index(crossS[i]))]
    limits = [0,0]
    crashed = 0
    trains = [tA,tB]
    alpha = ['e','f','g','h','i','j','k','l','m','n','o','p','q','r','t','u','v','w','y','z']
    count = 0
    for i in range(2):
        if len(trains[i]) != ''.join(new).lower().count(trains[i][0].lower()):
            print('broke before start')
            return 0,1
    #if train is reversed; do the reverse
    ind = []
    try:
        for i in range(2):
            if trains[i][0] == trains[i][0].upper():
                ind.append((new.index(trains[i][0])-1))
            else:
                ind.append((new.index(trains[i][-1])-len(trains[i])))
    except:
        print('ind error, default 0')
        return 0,1
    print(old)
    print(' ')
    while count < limit:
        count +=1
        if count>= debug:
            print(new)
            print(' ')
        if crashed != 0: break
        for train in range(len(trains)):
            if crashed!=0:break
            #if limiters
            for _ in range(1):
                if limits[train] > 0:
                    limits[train]-=1
                    break
                if trains[train][0] == trains[train][0].upper():#backwards
                    ind[train] -=1
                    if len(trains[train])>2:
                        pos = ind[train]+2
                    else:
                        pos = ind[train]+2
                    #dir = -1
                    if new[(pos-1)%len(new)] == 'S' and trains[train][0].lower() not in ['c','d']:
                        limits[train] = len(trains[train])-1
                    if new[(pos-1)%len(new)] in d3 and trains[train][0].lower() not in ['c','d']:
                        print('s found at '+str((pos-1)%len(new)))
                        limits[train] = len(trains[train])-1
                    new[(pos-1)%len(new)] = new[pos%len(new)]
                    new[pos%len(new)] = new[(pos+1)%len(new)]
                    new[(pos+len(trains[train])-1)%len(new)] = old[(pos+len(trains[train])-1)%len(old)]
                else:
                    ind[train] +=1
                    if len(trains[train]) > 2:
                        pos = ind[train]+len(trains[train])-1
                    else:
                        pos = ind[train]+len(trains[train])-1
                    #reversed pos
                    #dir = 1
                    if new[(pos+1)%len(new)] == 'S' and trains[train][0].lower() not in ['c','d']:
                        limits[train] = len(trains[train])-1
                    if new[(pos+1)%len(new)] in d3 and trains[train][0].lower() not in ['c','d']:
                        print('s found at '+str((pos+1)%len(new)))
                        limits[train] = len(trains[train])-1
                    new[(pos+1)%len(new)] = new[pos%len(new)]
                    new[pos%len(new)] = new[(pos+1)%len(new)].lower()
                    if train == 0:
                        new[(pos-len(trains[train])+1)%len(new)] = old[(pos+1-len(trains[train]))%len(old)]
                    else:
                        if new[(pos-len(trains[train])+1)%len(new)] in ['B','b','D','d']:
                            new[(pos-len(trains[train])+1)%len(new)] = old[(pos+1-len(trains[train]))%len(old)]
                
            #on second train finish, check crashes by len of trains, crosses
            
            if train != 0:
                
                #uniterupted string of bs and as and count is off
                for i in range(len(trains)):
                    #incorrect number of carts
                    if ''.join(new).upper().count(trains[i][0])+''.join(new).lower().count(trains[i][0]) != len(trains[i]):
                        
                        #chicken run or kamikazi
                        if any(x in ''.join(new).lower() for x in ['ab','ba','cd','dc','ad','da','bc','cb']):
##                            count-=1
                            print(new)
                            print('wrong cart crash')
                            #no header
                            if [x in ''.join(new) for x in ['A','B','C','D']].count(True) <2:
                                print('missing header')
                                if count == 1:
                                    return -2,1
                                return count,1
                            return count,1
                    #headers touching
                    if any(x in ''.join(new) for x in ['AB','BA','CD','DC','AD','DA','BC','CB']):
                        print(new)
                        print('headers about to touch')
                        #limit left
                        if sum(limits) > 0:
                            print('limit left')
                            return count+1,1
                        if count == 1:
                            return -2,1
                        return count+1,1
                #tbone   
                for i in d2:
                    if new[d2[i][0]] != old[d2[i][0]] and new[d2[i][1]] != old[d2[i][1]]:
                        print(new)
                        crashed+=1
                        return count,1
                for i in d3:
                    if new[d3[i][0]] != old[d3[i][0]] and new[d3[i][1]] != old[d3[i][1]]:
                        print(new)
                        crashed+=1
                        return count,1
    return count,crashed


def train(A,B):
    if 'x' not in A.lower():
        if A[0] == A[0].upper():
            A= 'A'+'a'*(len(A)-1)
        else:
            A= 'a'*(len(A)-1)+'A'
    else:
        if A[0] == A[0].upper():
            A = 'C'+'c'*(len(A)-1)
        else:
            A = 'c'*(len(A)-1)+'C'
    if 'x' not in B.lower():
        if B[0] == B[0].upper():
            B= 'B'+'b'*(len(B)-1)
        else:
            B= 'b'*(len(B)-1)+'B'
    else:
        if B[0] == B[0].upper():
            B = 'D'+'d'*(len(B)-1)
        else:
            B = 'd'*(len(B)-1)+'D'
    return A,B

def setup(track,tA,A,tB,B):
    track = track.replace('\\',']')
    arr = track.split('\n')
    for i in range(len(arr)):
        arr[i] = list(arr[i])
    new = ['-']
    cross = {}
    crossS = {}
    alpha = ['e','f','g','h','i','j','k','l','m','n','o','p','q','r','t','u','v','w','y','z']
    #get zero pos
    zero = []

    arr.insert(0,[' ' for i in range(len(arr[0]))])
    arr.append([' ' for i in range(len(arr[0]))])
    for i in range(len(arr)):
        arr[i].insert(0,' ')
        arr[i].append(' ')
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] != ' ' and arr[i][j] != ' ':
                zero = [i,j]
                break
        if zero != []:
            break
    print(zero)
    track = arr
    for i in range(len(track)):
        for j in range(len(track[i])):
            if track[i][j] == 'S':
                try:
                    if all(track[i+x][j+x] == ']' for x in [-1,1]) and all(track[i+x][j-x] == '/' for x in [-1,1]):
                        track[i][j] = 's'
                except:
                    pass
                try:
                    if all(track[i+x][j] == '|' for x in [-1,1]) and all(track[i][j+x] == '-' for x in [-1,1]):
                        track[i][j] = 's'
                except:
                    pass
    for i in track:
        print(''.join(i))
    #check array looks good
    ##start at top for clockwise rotation
    if track[zero[0]-1][zero[1]] != ' ':
        dire = 'U'
        x=zero[0]-1
        y=zero[1]
    elif track[zero[0]-1][zero[1]+1] != ' ':
        dire = 'UR'
        x=zero[0]-1
        y=zero[1]+1
    elif track[zero[0]][zero[1]+1] != ' ':
        dire = 'R'
        x=zero[0]
        y=zero[1]+1
    elif track[zero[0]+1][zero[1]+1] != ' ':
        dire = 'DR'
        x=zero[0]+1
        y=zero[1]+1
    elif track[zero[0]+1][zero[1]] != ' ':
        dire = 'D'
        x=zero[0]+1
        y=zero[1]
    elif track[zero[0]+1][zero[1]-1] != ' ':
        dire = 'DL'
        x=zero[0]+1
        y=zero[1]-1
    elif track[zero[0]][zero[1]-1] != ' ':
        dire = 'L'
        x=zero[0]
        y=zero[1]-1
    elif track[zero[0]-1][zero[1]-1] != ' ':
        dire = 'UL'
        x=zero[0]-1
        y=zero[1]-1
    print(x,y)
    
    while x != zero[0] or y!=zero[1]:
        if dire == 'R': #-]/S+
            if track[x][y] == '-':
                if track[x][y+1] in [']','-','S','s','+','/']:
                    new.append('-')
                    y=y+1
            elif track[x][y] == ']':
                if track[x+1][y] in ['|','+','S','s','/']:
                    dire = 'D'
                    new.append('-')
                    x=x+1
                elif track[x+1][y+1] in [']','S','X','s']:
                    dire = 'DR'
                    new.append('-')
                    x=x+1
                    y=y+1
            elif track[x][y] == '/':
                if track[x-1][y] in ['|','+','S',']','s']:
                    dire = 'U'
                    new.append('-')
                    x=x-1
                elif track[x-1][y+1] in ['/','S','X','s']:
                    dire = 'UR'
                    new.append('-')
                    x=x-1
                    y=y+1
            #S+
            elif track[x][y] == 'S':
                if track[x][y+1] in ['/',']','+','-','S']:
                    new.append('S')
                    y=y+1
            elif track[x][y] == '+':
                if (x,y) in cross:
                    new.append(cross[(x,y)])
                else:
                    cross[(x,y)] = alpha[len(cross)]
                    new.append(cross[(x,y)])
                y=y+1
            elif track[x][y] == 's':
                if (x,y) in cross:
                    new.append(cross[(x,y)])
                else:
                    cross[(x,y)] = alpha[len(cross)]
                    new.append(cross[(x,y)])
                if (x,y) not in crossS:
                    crossS[(x,y)] = alpha[len(cross)-1]
                y=y+1
        if dire == 'L': #-]/S+
            if track[x][y] == '-':
                if track[x][y-1] in [']','/','-','S','+','s']:
                    new.append('-')
                    y=y-1
            elif track[x][y] == ']':
                if track[x-1][y] in ['|','/','S','+','s']:
                    dire = 'U'
                    x=x-1
                    new.append('-')
                elif track[x-1][y-1] in ['X','S',']','s']:
                    dire = 'UL'
                    x=x-1
                    y=y-1
                    new.append('-')
            elif track[x][y] == '/':
                if track[x+1][y] in ['|',']','S','+','s']:
                    dire = 'D'
                    x=x+1
                    new.append('-')
                elif track[x+1][y-1] in ['S','X','/','s']:
                    dire = 'DL'
                    x=x+1
                    y=y-1
                    new.append('-')
            #S+
            elif track[x][y] == 'S':
                if track[x][y-1] in ['/',']','+','-','S']:
                    new.append('S')
                    y=y-1
            elif track[x][y] == '+':
                if (x,y) in cross:
                    new.append(cross[(x,y)])
                else:
                    cross[(x,y)] = alpha[len(cross)]
                    new.append(cross[(x,y)])
                y=y-1
            elif track[x][y] == 's':
                if (x,y) in cross:
                    new.append(cross[(x,y)])
                else:
                    cross[(x,y)] = alpha[len(cross)]
                    new.append(cross[(x,y)])
                if (x,y) not in crossS:
                    crossS[(x,y)] = alpha[len(cross)-1]
                y=y-1
        if dire == 'U':
            if track[x][y] == '|':
                if track[x-1][y] in ['|','+',']','/','S','s']:
                    x=x-1
                    new.append('-')
            elif track[x][y] == ']':
                if track[x][y-1] in ['-','S','+','/','s']:
                    y=y-1
                    dire = 'L'
                    new.append('-')
                elif track[x-1][y-1] in ['S','X',']','s']:
                    x=x-1
                    y=y-1
                    dire = 'UL'
                    new.append('-')
            elif track[x][y] == '/':
                if track[x][y+1] in ['-','S','+',']','s']:
                    y=y+1
                    new.append('-')
                    dire = 'R'
                elif track[x-1][y+1] in ['S','X','/','s']:
                    x=x-1
                    y=y+1
                    dire = 'UR'
                    new.append('-')
            #S+
            elif track[x][y] == 'S':
                if track[x-1][y] in ['/',']','+','|','S']:
                    new.append('S')
                    x=x-1
            elif track[x][y] == '+':
                if (x,y) in cross:
                    new.append(cross[(x,y)])
                else:
                    cross[(x,y)] = alpha[len(cross)]
                    new.append(cross[(x,y)])
                x=x-1
            elif track[x][y] == 's':
                if (x,y) in cross:
                    new.append(cross[(x,y)])
                else:
                    cross[(x,y)] = alpha[len(cross)]
                    new.append(cross[(x,y)])
                if (x,y) not in crossS:
                    crossS[(x,y)] = alpha[len(cross)-1]
                x=x-1
        if dire == 'D':
            if track[x][y] == '|':
                if track[x+1][y] in ['|','+',']','/','S','s']:
                    x=x+1
                    new.append('-')
            elif track[x][y] == ']':
                if track[x][y+1] in ['-','S','+','/','s']:
                    y=y+1
                    dire = 'R'
                    new.append('-')
                elif track[x+1][y+1] in ['S','X',']','s']:
                    x=x+1
                    y=y+1
                    new.append('-')
                    dire = 'DR'
            elif track[x][y] == '/':
                if track[x][y-1] in ['-','S','+',']','s']:
                    y=y-1
                    new.append('-')
                    dire = 'L'
                elif track[x+1][y-1] in ['S','X','/','s']:
                    x=x+1
                    y=y-1
                    new.append('-')
                    dire = 'DL'
            #S+
            elif track[x][y] == 'S':
                if track[x+1][y] in ['/',']','+','|','S']:
                    new.append('S')
                    x=x+1
            elif track[x][y] == '+':
                if (x,y) in cross:
                    new.append(cross[(x,y)])
                else:
                    cross[(x,y)] = alpha[len(cross)]
                    new.append(cross[(x,y)])
                x=x+1
            elif track[x][y] == 's':
                if (x,y) in cross:
                    new.append(cross[(x,y)])
                else:
                    cross[(x,y)] = alpha[len(cross)]
                    new.append(cross[(x,y)])
                if (x,y) not in crossS:
                    crossS[(x,y)] = alpha[len(cross)-1]
                x=x+1
        if dire == 'UR':
            if track[x][y] == '/':
                if track[x][y+1] in ['-','S','+',']','s']:
                    y=y+1
                    dire = 'R'
                    new.append('-')
                elif track[x-1][y] in ['|','S','+',']','s']:
                    x=x-1
                    dire = 'U'
                    new.append('-')
                elif track[x-1][y+1] in ['S','X','/','s']:
                    x=x-1
                    y=y+1
                    new.append('-')
            #SX
            elif track[x][y] == 'S':
                new.append('S')
                y=y+1
                x=x-1
            elif track[x][y] == 'X':
                if (x,y) in cross:
                    new.append(cross[(x,y)])
                else:
                    cross[(x,y)] = alpha[len(cross)]
                    new.append(cross[(x,y)])
                y=y+1
                x=x-1
            elif track[x][y] == 's':
                if (x,y) in cross:
                    new.append(cross[(x,y)])
                else:
                    cross[(x,y)] = alpha[len(cross)]
                    new.append(cross[(x,y)])
                if (x,y) not in crossS:
                    crossS[(x,y)] = alpha[len(cross)-1]
                y=y+1
                x=x-1
        if dire == 'UL':
            if track[x][y] == ']':
                if track[x][y-1] in ['-','S','+','/','s']:
                    y=y-1
                    dire = 'L'
                    new.append('-')
                elif track[x-1][y] in ['|','S','+','/','s']:
                    x=x-1
                    dire = 'U'
                    new.append('-')
                elif track[x-1][y-1] in ['S','X',']','s']:
                    x=x-1
                    y=y-1
                    new.append('-')
            #SX
            elif track[x][y] == 'S':
                new.append('S')
                y=y-1
                x=x-1
            elif track[x][y] == 'X':
                if (x,y) in cross:
                    new.append(cross[(x,y)])
                else:
                    cross[(x,y)] = alpha[len(cross)]
                    new.append(cross[(x,y)])
                y=y-1
                x=x-1
            elif track[x][y] == 's':
                if (x,y) in cross:
                    new.append(cross[(x,y)])
                else:
                    cross[(x,y)] = alpha[len(cross)]
                    new.append(cross[(x,y)])
                if (x,y) not in crossS:
                    crossS[(x,y)] = alpha[len(cross)-1]
                y=y-1
                x=x-1
        if dire == 'DL':
            if track[x][y] == '/':
                if track[x][y-1] in ['-','S','+',']','s']:
                    y=y-1
                    dire = 'L'
                    new.append('-')
                elif track[x+1][y] in ['|','S','+',']','s']:
                    x=x+1
                    dire = 'D'
                    new.append('-')
                elif track[x+1][y-1] in ['S','X','/','s']:
                    x=x+1
                    y=y-1
                    new.append('-')
            #SX
            elif track[x][y] == 'S':
                new.append('S')
                y=y-1
                x=x+1
            elif track[x][y] == 'X':
                if (x,y) in cross:
                    new.append(cross[(x,y)])
                else:
                    cross[(x,y)] = alpha[len(cross)]
                    new.append(cross[(x,y)])
                y=y-1
                x=x+1
            elif track[x][y] == 's':
                if (x,y) in cross:
                    new.append(cross[(x,y)])
                else:
                    cross[(x,y)] = alpha[len(cross)]
                    new.append(cross[(x,y)])
                if (x,y) not in crossS:
                    crossS[(x,y)] = alpha[len(cross)-1]
                y=y-1
                x=x+1
        if dire == 'DR':
            if track[x][y] == ']':
                if track[x][y+1] in ['-','S','+','/','s']:
                    y=y+1
                    dire = 'R'
                    new.append('-')
                elif track[x+1][y] in ['|','S','+','/','s']:
                    x=x+1
                    dire = 'D'
                    new.append('-')
                elif track[x+1][y+1] in ['S','X',']','s']:
                    x=x+1
                    y=y+1
                    new.append('-')
            #SX
            elif track[x][y] == 'S':
                new.append('S')
                y=y+1
                x=x+1
            elif track[x][y] == 'X':
                if (x,y) in cross:
                    new.append(cross[(x,y)])
                else:
                    cross[(x,y)] = alpha[len(cross)]
                    new.append(cross[(x,y)])
                y=y+1
                x=x+1
            elif track[x][y] == 's':
                if (x,y) in cross:
                    new.append(cross[(x,y)])
                else:
                    cross[(x,y)] = alpha[len(cross)]
                    new.append(cross[(x,y)])
                if (x,y) not in crossS:
                    crossS[(x,y)] = alpha[len(cross)-1]
                y=y+1
                x=x+1
    old = deepcopy(new)
    if tA[0] == tA[0].upper():
        for i in range(len(tA)):
            new[(A+i)%len(new)] = tA[i]
    else:
        for i in range(len(tA)):
            new[(A+i-len(tA)+1)%len(new)] = tA[i]
    if tB[0] == tB[0].upper():
        for i in range(len(tB)):
            new[(B+i)%len(new)] = tB[i]
    else:
        for i in range(len(tB)):
            new[(B+i-len(tB)+1)%len(new)] = tB[i]
    return new,cross,old,crossS
debug = 9999
