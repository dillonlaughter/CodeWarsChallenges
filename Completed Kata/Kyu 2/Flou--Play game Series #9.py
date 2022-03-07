import time
global starttime,starttime1,starttime2
#starttime = time.time()
global endtime
def get_inner(nested):
    if all(type(x) == list for x in nested):
        for x in nested:
            for y in get_inner(x):
                yield y
    else:
        yield nested
def play_flou(game_map):

    starttime = time.time()
    move = 0
    fin = run(game_map,move)
    arr = []
    if type(fin) == type(None):
        return
    fin = list(get_inner(fin))
    
    for j in fin:
        p = [j[0][0]-1,j[0][1]-1]
        arr.append(tuple([p[0],p[1],j[1]]))
    return arr


import re
import numpy as np
from copy import deepcopy
def basics(num):
    #global players,arr1,players
    arr = big_list[num].split('\n')
    for i in range(len(arr)):
        arr[i] = list(arr[i])
    arr1 = np.asarray(arr)
    players = list(zip(*np.where(arr1 == 'B')))

def runner():
    global times_all
    times_all = []
    timer_final = time.time()
    for i in range(len(big_list)):
        play_flou(big_list[i])
    print('took:',time.time()-timer_final)


def compare2func(fun1,fun2,tries,*args):
    times = []
    time1 = time.time()
    for _ in range(tries):
        a =fun1(*args)
    times.append(time.time()-time1)
    time2 = time.time()
    for _ in range(tries):
        b = fun2(*args)
    times.append(time.time()-time2)
    time2 = time.time()
    for _ in range(tries):
        b = fun2(*args)
    times.append(time.time()-time2)
    time1 = time.time()
    for _ in range(tries):
        a =fun1(*args)
    times.append(time.time()-time1)
    print('fun1 took: ',times[0]+times[2])
    print('fun2 took: ',times[1]+times[3])
  
def run(arr,move):
    game_map = arr.split('\n')
    for i in range(len(game_map)):
        game_map[i] = list(game_map[i])
    arr1 = np.asarray(game_map)
    players = list(zip(*np.where(arr1 == 'B')))
    for player in range(len(players)):
        players[player] = [players[player][0],players[player][1]]

    for i in range(len(players)):
        if all(game_map[players[i][0]+x[0]][players[i][1]+x[1]] != '.' for x in [[-1,0],[0,-1],[1,0],[0,1]]):
            return
    nparr = np.asarray(game_map).astype('<U2')
    solution = new_try(players,nparr,move)
    return solution
        
##def getvalid(player,arr):
##    res =[]
##    if arr[player[0]][player[1]+1] == '.': res.append('Right')
##    if arr[player[0]][player[1]-1] == '.': res.append('Left')
##    if arr[player[0]-1][player[1]] == '.': res.append('Up')
##    if arr[player[0]+1][player[1]] == '.': res.append('Down')
##    return res
def getdirections(player,arr):
    ress = ['Right','Left','Up','Down']
    res = []
    opt = [[0,1],[0,-1],[-1,0],[1,0]]
    for i in range(len(opt)):
        if arr[player[0]+opt[i][0]][player[1]+opt[i][1]] == '.':
            res.append(ress[i])
    return res
    
def moveplayer(player,moveindex,direction,both):
    count=0
    while count != 4:
        if direction =='Left':
            match = re.match('(\.){1,}',''.join(both[player[0]][0:player[1]][::-1]))
            if match:
                both[player[0]][player[1]-len(match.group()):player[1]] = str(moveindex)
                player = [player[0],player[1]-len(match.group())]
                if both[player[0]-1][player[1]] == '.':
                    direction = 'Up'
                else:
                    count=4
            else:count=4
        if direction =='Right':
            match = re.match('(\.){1,}',''.join(both[player[0]][player[1]+1:]))
            if match:
                both[player[0]][player[1]+1:player[1]+1+len(match.group())] = str(moveindex)
                player = [player[0],player[1]+len(match.group())]
                if both[player[0]+1][player[1]] == '.':
                    direction = 'Down'
                else:
                    count=4
            else:count=4
        if direction =='Up':
            match = re.match('(\.){1,}',''.join(both[:,player[1]][0:player[0]][::-1]))
            if match:
                both[:,player[1]][player[0]-len(match.group()):player[0]] = str(moveindex)
                player = [player[0]-len(match.group()),player[1]]
                if both[player[0]][player[1]+1] == '.':
                    direction = 'Right'
                else:
                    count=4
            else:count=4
        if direction =='Down':
            match = re.match('(\.){1,}',''.join(both[:,player[1]][player[0]+1:]))
            if match:
                both[:,player[1]][player[0]+1:player[0]+1+len(match.group())] = str(moveindex)
                player = [player[0]+len(match.group()),player[1]]
                if both[player[0]][player[1]-1] == '.':
                    direction = 'Left'
                else:
                    count=4
            else:count=4

    return both
        
        
##def checkarr(arr):
##    if len(list(zip(*np.where(arr=='.')))) > 0:
##        return False
##    return True
##def checkarr(arr):
##    if '.' in arr:
##        return False
##    return True

def show_me(gm,sol,num=-1):
    if num != -1:
        gm = big_list[num]
    arr = gm.split('\n')
    for i in range(len(arr)):
        arr[i] = list(arr[i])
    arr1 = np.asarray(arr)
    move = 0
    for i in sol:
        arr = moveplayer([i[0][0]+1,i[0][1]+1],move,i[1],arr1)
        move+=1
    for i in arr:
        print(i)
def new_try(players,arr,move):
    solution = []
    for i in range(len(players)):
        player = players[i]
        directions = getdirections(player,arr)
        if len(directions) == 0:
            return []
        for direction in directions:
            solution.append([player,direction])
            move+=1
            moveindex = move #?
            arr = moveplayer(player,moveindex,direction,arr)
            otherplayers = players[0:i]+players[i+1:]#?
            if len(otherplayers) == 0:
                if '.' not in arr:
                    return solution
            else:
                tryagain = new_try(otherplayers,arr,move)
                if len(tryagain) > 0:
                    return [solution,tryagain]
            arr[arr==str(moveindex)] = '.'
            solution.pop()
    return solution
