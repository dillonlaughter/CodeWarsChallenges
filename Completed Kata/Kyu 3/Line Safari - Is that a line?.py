import numpy as np
from copy import deepcopy

def line(grid):
    global arra
    arra = []
    for i in range(len(grid)):
        grid[i] = list(grid[i])
    arr = np.asarray(grid)
    arr = np.pad(arr, pad_width=1, mode='constant', constant_values=' ')
    players = list(zip(*np.where(arr=='X')))
    for i in range(len(players)):
        players[i] = [players[i][0],players[i][1]]
    arr = arr.astype('<U2')
    arr1 = deepcopy(arr)
    for i in range(len(players)):
        move = 0
        arr2 = deepcopy(arr)
        arra.append([])
        solution = new_try(arr2,players[i],'?',move,arr1)
    if [True] in arra:
        return True
    return False

def getvaliddirections(arr,player,oldarr,direction='?'):
    res = []
    ress = ['up','down','left','right']
    opt = [[-1,0],[1,0],[0,-1],[0,1]]
    lookfor = [['+','X','|'],['+','X','|'],['-','+','X'],['-','+','X']]
    dic = {'left':'right','right':'left','up':'down','down':'up'}
    if direction == '?':
        for i in range(len(opt)):
            if arr[player[0]+opt[i][0]][player[1]+opt[i][1]] in lookfor[i]:
                res.append(ress[i])
    else:
        tres = []
        if oldarr[player[0]][player[1]] =='-':
            if direction == 'left':
                if arr[player[0]][player[1]-1] in ['-','X','+']:
                    res.append('left')
            if direction == 'right':
                if arr[player[0]][player[1]+1] in ['-','X','+']:
                    res.append('right')
        elif oldarr[player[0]][player[1]] =='|':
            if direction == 'up':
                if arr[player[0]-1][player[1]] in ['|','X','+']:
                    res.append('up')
            if direction == 'down':
                if arr[player[0]+1][player[1]] in ['|','X','+']:
                    res.append('down')
        elif oldarr[player[0]][player[1]] =='+':          
            for i in range(len(opt)):
                if arr[player[0]+opt[i][0]][player[1]+opt[i][1]] in lookfor[i]:
                    if direction != ress[i]:
                        if direction != dic[ress[i]]:
                            res.append(ress[i])
    return res

def moveplayer(arr,player,direction,moveindex):
    arr[player[0]][player[1]] = str(moveindex)
    if direction == 'left':
        player = [player[0],player[1]-1]
    elif direction == 'right':
        player = [player[0],player[1]+1]
    elif direction == 'up':
        player = [player[0]-1,player[1]]
    elif direction == 'down':
        player = [player[0]+1,player[1]]
    return arr,player

def new_try(arr,player,odirection,move,oldarr):
    global arra
    solution = []
    directions = getvaliddirections(arr,player,oldarr,odirection)
    if len(directions) > 1:
        arra[-1].append(False)
        return []
    for direction in directions:
        solution.append(direction)
        move+=1
        moveindex = move
        arr,player = moveplayer(arr,player,direction,moveindex)
        if arr[player[0]][player[1]] == 'X':
            if not ('-' in arr or '|' in arr):
                arra[-1].append(True)
        else:  
            tryagain = new_try(arr,player,direction,move,oldarr)
            if False in arra[-1]:
                return solution
            if len(tryagain)>0:
                return [solution,tryagain]
    return solution
