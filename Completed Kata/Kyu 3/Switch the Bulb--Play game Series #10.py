import numpy as np
Checker.WITH_CANVAS = False     # Use this if you have troubles with buffer limit errors


def switch_bulbs(game_map):
    global board,bulbs,bulb,others,path
    bulbs = {}
    others = {}
    othersx = {}
    board = game_map.split('\n')
    
    for i in range(len(board)):
        board[i] = list(board[i])
    board = np.array(board)
    bulbs_ = np.column_stack(np.where(board=='B'))
    for i in range(len(bulbs_)):
        bulbs[i] = bulbs_[i]
    for i in bulbs:
        othersx[i] = get_other_bulbs(board,bulbs[i],bulbs)
    for i in othersx:
        for j in bulbs:
            for k in othersx[i]:
                if np.all(k == bulbs[j]):
                    if i not in others:
                        others[i] = []
                    others[i].append(j)
    path = find_path_through_all(bulbs.keys(), others)
    if path:
        fin = []
        for i in path:
            fin.append((bulbs[i]-1).tolist())
        return fin
    else:
        return None


def find_path_through_all(points, neighbors):
    def backtrack(current_node, visited):
        # Base Case: All points visited
        if len(visited) == len(points):
            return visited
        
        # Try all neighbors of the current point
        for neighbor in neighbors.get(current_node, []):
            if neighbor not in visited:
                # Add to path and recurse
                visited.append(neighbor)
                result = backtrack(neighbor, visited)
                if result:
                    return result
                # Backtrack: remove if no path found through this neighbor
                visited.pop()
        return None

    # Try starting from every possible point
    for start_node in points:
        path = backtrack(start_node, [start_node])
        if path:
            return path
    return None
        
def get_other_bulbs(board,bulb,bulbs):
    others = []
    #downleft
    i=1
    while bulb[0]+i <len(board) and bulb[1]-i >0:
        if board[bulb[0]+i,bulb[1]-i] == 'B':
            others.append([bulb[0]+i,bulb[1]-i])
            break
        i+=1
    #upright
    i=1
    while bulb[0]-i >0 and bulb[1]+i <len(board[0]):
        if board[bulb[0]-i,bulb[1]+i] == 'B':
            others.append([bulb[0]-i,bulb[1]+i])
            break
        i+=1
    #downright
    i=1
    while bulb[0]+i <len(board) and bulb[1]+i <len(board[0]):
        if board[bulb[0]+i,bulb[1]+i] == 'B':
            others.append([bulb[0]+i,bulb[1]+i])
            break
        i+=1
    #upleft
    i=1
    while bulb[0]-i >0 and bulb[1]-i >0:
        if board[bulb[0]-i,bulb[1]-i] == 'B':
            others.append([bulb[0]-i,bulb[1]-i])
            break
        i+=1
    #down
    i=1
    while bulb[0]+i <len(board):
        if board[bulb[0]+i,bulb[1]] == 'B':
            others.append([bulb[0]+i,bulb[1]])
            break
        i+=1
    #up
    i=1
    while bulb[0]-i >0:
        if board[bulb[0]-i,bulb[1]] == 'B':
            others.append([bulb[0]-i,bulb[1]])
            break
        i+=1
    #right
    i=1
    while bulb[1]+i <len(board[0]):
        if board[bulb[0],bulb[1]+i] == 'B':
            others.append([bulb[0],bulb[1]+i])
            break
        i+=1
    #left
    i=1
    while bulb[1]-i >0:
        if board[bulb[0],bulb[1]-i] == 'B':
            others.append([bulb[0],bulb[1]-i])
            break
        i+=1
    others2 = []
    for i in others:
        others2.append([int(i[0]),int(i[1])])
    return others2
