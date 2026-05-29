import re
from itertools import groupby,permutations
from itertools import chain as itch
import string
import copy

regexname = '[A-z]+'

def find_out_mr_wrong(conversation_):
    fin = find_out_mr_wrong1(conversation_)
    if fin != None:
        return people_rename[fin]
    return fin

def find_out_mr_wrong1(conversation_):
    print(conversation_)
    #deleting all globals
    for i in ['arr','solutions','alt_pos','liar','conversation']:
        if i in globals():del globals()[i]

    global conversation,people,people_rename
    conversation = conversation_
    solutions = []
    people = []
    for i in conversation:
        name = re.findall(regexname+':',i)[0][:-1]
        people.append(name)
    people = sorted(list(set(people)))
    people_rename = {}
    for i in range(len(people)):
        people_rename[(string.ascii_uppercase+string.ascii_lowercase)[i]] = people[i]
    for i in range(len(conversation)):
        for j in people_rename:
            conversation[i] = conversation[i].replace(people_rename[j],j)
    people = people_rename.keys()

    known_truthers = {}

    #place easys and set up alt_pos
    arr = []
    for liar in people:
        alt_pos = {}
        for i in people:
            alt_pos[i] = ['_','_']
        arr = ['_' for i in range(len(people))]

        arr,alt_pos,error1,liars_words = place_easy(arr,alt_pos,liar)
        if error1:
            known_truthers[liar]=''
            continue
        arr,alt_pos,error1 = alt_check(arr,alt_pos)
        if error1:
            known_truthers[liar]=''
            continue

        if len(''.join(list(set(arr))).replace('_','')) != len(''.join(arr).replace('_','')):
            known_truthers[liar]=''
            continue
        
        if arr.count('_') == 1:
            for i in people:
                if i not in arr:
                    arr[arr.index('_')] = i
                    break

        chains, error = get_chains(arr,alt_pos,i)
        if error:
            known_truthers[liar]=''
            continue

        
        error = liar_validation(arr,alt_pos,liars_words,liar)
        if error:
            known_truthers[liar]=''
            continue


        error = final_check(arr,alt_pos,liar,liars_words)
        if error:
            known_truthers[liar]=''
            continue


        works = permutate(arr,chains,alt_pos,liar,liars_words)
        if not works:
            known_truthers[liar]=''
            continue

    fin = list(set(people)-set(known_truthers.keys()))
    match len(fin):
        case 0:
            return None
        case 1:
            return fin[0]
        case _:
            return None
        


def permutate(arr,chains,alt_pos,liar,liars_words):
    result = [(key, len(list(group))) for key, group in groupby(arr)]
    gaps = []
    for i in result:
        if i[0] == '_':
            gaps.append(i[1])
    before_perms = filtperm(chains,arr.count('_'))

    perms = []
    for option in before_perms:
        brk=0
        values = []
        for i in option:
            values.append(len(i))
        ind = 0
        total = 0
        for i in range(len(values)):
            if len(gaps) > ind:
                target = gaps[ind]
                if values[i] + total < target:
                    total+=values[i]
                elif values[i] + total == target:
                    ind+=1
                    total = 0
                elif values[i] + total > target:
                    brk = 1
                    break
        if brk:continue
        perms.append([item for sublist in option for item in sublist])
    for i in perms:
        arr_ = copy.deepcopy(arr)
        ind = 0
        for j in range(len(arr)):
            if arr[j] == '_':
                arr_[j] = i[ind]
                ind+=1
        error = final_check(arr_,alt_pos,liar,liars_words)
        if not error:
            return 1
    return 0


        
def filtperm(arr, length):

    all_perms = permutations(arr)

    valid_perms = [p for p in all_perms if sum(len(sublist) for sublist in p) == length]

    return valid_perms   
    
def get_chains(arr,alt_pos,i):
    error = 0
    currently_in_chain = []
    chains1 = []
    chains = []
    for i in alt_pos:
        if i not in currently_in_chain:
            if i not in arr:
                error = 0
                chain_start,error = chain_first(arr,alt_pos,i)
                if chain_start == '':
                    chains1.append([i])
                    continue
                if error:return 1,error
                chain2,error = chain_check(arr,alt_pos,chain_start,[])
                del chain_start
                currently_in_chain+=copy.deepcopy(chain2)
                chains1.append(copy.deepcopy(chain2))
                del chain2

    return chains1,error

def chain_first(arr,alt_pos,i,chain='',depth=0):
    if depth > len(arr):return i,1
    error = 0
    if i not in arr:
        if alt_pos[i] == [i,i] or (alt_pos[i].count(alt_pos[i][0]) == 2 and alt_pos[i][0] != '_'):
            return i,1
        if alt_pos[i] != ['_','_']:
            if alt_pos[i][0] != '_':#first neighnor
                if alt_pos[i][0] not in chain:
                    chain,error = chain_first(arr,alt_pos,alt_pos[i][0],chain,depth+1)
                else:
                    error = 1
            else:
                #first in chain
                return i,error
    return chain,error
    
def chain_check(arr,alt_pos,i,chain = []):
    error = 0
    chain.append(i)
    if alt_pos[i][1] != '_':#new neighnor
        if alt_pos[i][1] not in chain:
            chain,error = chain_check(arr,alt_pos,alt_pos[i][1],chain)
        else:
            return chain,error
    return chain,error

def runner(people,arr,alt_pos,liar,liars_words):
    not_in_arr = list(set(people)-set(arr))
    perm = permutations(not_in_arr)
    for i in perm:
        arr_ = copy.deepcopy(arr)
        ind = 0
        for j in range(len(arr)):
            if arr[j] == '_':
                arr_[j] = i[ind]
                ind+=1
        #new potential arrangement set up
        error = final_check(arr_,alt_pos,liar,liars_words)
        if not error:
            return 1
    return 0
        
    
    

def final_check(arr,alt_pos,liar,liars_words):
    error = check_conversation(arr,liar)
    if error:return 1
    error = liar_validation(arr,alt_pos,liars_words,liar)
    if error:return 1
    return 0

def check_conversation(arr,liar):
    error = 0
    for word in conversation:
        if liar+':' in word:
            continue
        if "I'm in" in word:
            pos = int(re.findall('[0-9]+',word)[0])-1
            if arr[pos] != re.findall(regexname+':',word)[0][:-1]:
                error =1
                break
        if 'The man behind' in word:
            if re.findall(regexname+':',word)[0][:-1] in arr:
                ind = arr.index(re.findall(regexname+':',word)[0][:-1])
                if ind+1 < len(arr):
                    if arr[ind+1] != re.findall(' '+regexname+'\.',word)[0][1:-1]:
                        error =1
                        break
                else:
                    error =1
                    break
        if 'The man in front' in word:
            if re.findall(regexname+':',word)[0][:-1] in arr:
                ind = arr.index(re.findall(regexname+':',word)[0][:-1])
                if ind-1 >= 0:
                    if arr[arr.index(re.findall(regexname+':',word)[0][:-1])-1] != re.findall(' '+regexname+'\.',word)[0][1:-1]:
                        error =1
                        break
                else:
                    error =1
                    break
        if 'There is' in word or 'There are' in word:
            if 'in front' in word:
                pos = int(re.findall('[0-9]+',word)[0])
                if arr[pos] != re.findall(regexname+':',word)[0][:-1]:
                    error =1
                    break
            if 'behind' in word:
                pos = len(people) - int(re.findall('[0-9]+',word)[0]) - 1
                if arr[pos] != re.findall(regexname+':',word)[0][:-1]:
                    error =1
                    break
    return error
    



def liar_validation(arr,alt_pos,liars_words,liar):
    error = 0
    for word in liars_words:
        if "I'm in" in word:
            pos = int(re.findall('[0-9]+',word)[0])-1
            if arr[pos] in [liar]:
                error = 1
                break
        if 'The man behind' in word:
            other = re.findall(' '+regexname+'\.',word)[0][1:-1]
            if alt_pos[other][0] in [liar]:
                error = 1
                break
            try:
                if liar in arr:
                    if arr[arr.index(liar)+1] == other:
                        error=1
                        break
            except:pass
        if 'The man in front' in word:
            other = re.findall(' '+regexname+'\.',word)[0][1:-1]
            if alt_pos[other][1] in [liar]:
                error = 1
                break
            try:
                if liar in arr:
                    if arr[arr.index(liar)-1] == other and arr.index(liar)-1 >=0:
                        error=1
                        break
            except:pass
        if 'There is' in word or 'There are' in word:
            if 'in front' in word:
                pos = int(re.findall('[0-9]+',word)[0]) 
                if arr[pos] in [liar]:
                    error = 1
                    break
            if 'behind' in word:
                pos = len(people) - int(re.findall('[0-9]+',word)[0]) - 1
                if arr[pos] in [liar]:
                    error = 1
                    break
    return error

def place_easy(arr,alt_pos,liar):
    error = 0
    liars_words = []
    for word in conversation:
        if liar+':' in word:
            liars_words.append(word) 
            continue
        if "I'm in" in word:
            pos = int(re.findall('[0-9]+',word)[0])-1
            arr,alt_pos,error = placing(re.findall(regexname+':',word)[0][:-1],pos,arr,alt_pos)
            if error:break
        if 'The man behind' in word:
            arr,alt_pos,error = altadd(re.findall(regexname+':',word)[0][:-1],1,re.findall(' '+regexname+'\.',word)[0][1:-1],arr,alt_pos)
            if error:break
        if 'The man in front' in word:
            arr,alt_pos,error = altadd(re.findall(regexname+':',word)[0][:-1],0,re.findall(' '+regexname+'\.',word)[0][1:-1],arr,alt_pos)
            if error:break
        if 'There is' in word or 'There are' in word:
            if 'in front' in word:
                pos = int(re.findall('[0-9]+',word)[0])
                arr,alt_pos,error = placing(re.findall(regexname+':',word)[0][:-1],pos,arr,alt_pos)
                if error: break
            if 'behind' in word:
                pos = len(people) - int(re.findall('[0-9]+',word)[0]) - 1
                arr,alt_pos,error = placing(re.findall(regexname+':',word)[0][:-1],pos,arr,alt_pos)
                if error:break
    return arr,alt_pos,error,liars_words

def placing(person,place,arr_,alt_pos_):
    error = 0
    place = int(place)
    if arr_[place] == '_':
        arr_[place] = person
        for i in range(2):
            if alt_pos_[person][i] != '_':
                if i == 0 and place-1>=0:
                    arr_,alt_pos_,error = placing(alt_pos_[person][i],place-1,arr_,alt_pos_)
                elif place+1<len(arr_):
                    arr_,alt_pos_,error = placing(alt_pos_[person][i],place+1,arr_,alt_pos_)
    elif arr_[place] != '_' and arr_[place] == person:
        pass
    else: error = 1
    if place-1>0:
        if arr_[place-1] != '_':
            arr_,alt_pos_,error = altadd(person,0,arr_[place-1],arr_,alt_pos_)
    if place+1<len(arr_):
        if arr_[place+1] != '_':
            arr_,alt_pos_,error = altadd(person,1,arr_[place+1],arr_,alt_pos_)
    return arr_,alt_pos_,error

def altadd(person,place,other,arr_,alt_pos_):
    error = 0
    if place == 0:
        if alt_pos_[person][place] == '_':
            alt_pos_[person][place] = other
            if person in arr_:
                if arr_.index(person)-1 >= 0:
                    arr_,alt_pos_,error1 = placing(other,arr_.index(person)-1,arr_,alt_pos_)
                    if error1:error=1
            if alt_pos_[other][1] == '_':
                alt_pos_[other][1] = person
            elif alt_pos_[other][1] == person:
                pass
            else:
                error = 1
        elif alt_pos_[person][place] == other:
            pass
        else:
            error = 1
    if place == 1:
        if alt_pos_[person][place] == '_':
            alt_pos_[person][place] = other
            if person in arr_:
                if arr_.index(person)+1 < len(arr_):
                    arr_,alt_pos_,error1 = placing(other,arr_.index(person)+1,arr_,alt_pos_)
                    if error1:error=1
            if alt_pos_[other][0] == '_':
                alt_pos_[other][0] = person
            elif alt_pos_[other][0] == person:
                pass
            else:
                error = 1
        elif alt_pos_[person][place] == other:
            pass
        else:
            error = 1
    return arr_,alt_pos_,error

def alt_check(arr,alt_pos):
    error = 0
    b=0
    while b==0:
        b=1
        arr,alt_pos,error1,b = neighbor_place(arr,alt_pos)
        if error1:return arr,alt_pos,1

    return arr,alt_pos,error
    


def neighbor_place(arr_,alt_pos_):
    b,error=1,0
    for i in alt_pos_:
        if alt_pos_[i][0] != '_':
            if alt_pos_[i][0] in arr_:
                if i in arr_:
                    if arr_.index(i) -1 >=0:
                        if arr_[arr_.index(i)-1] == '_':
                            arr_[arr_.index(i)-1] = alt_pos_[i][0]
                            b=0
                        elif arr_[arr_.index(i)-1] == alt_pos_[i][0]:
                            pass
                        else:
                            error = 1
                    else:
                        error = 1
                elif i not in arr_:
                    if arr_.index(alt_pos_[i][0])+1 < len(arr_):
                        if arr_[arr_.index(alt_pos_[i][0])+1] != '_':
                            pass
                        else:
                            arr_[arr_.index(alt_pos_[i][0])+1] = i
                            b=0
                    else:
                        error = 1
            elif alt_pos_[i][0] not in arr_:
                if i in arr_:
                    if arr_.index(i) -1 >=0:
                        if arr_[arr_.index(i)-1] == '_':
                            arr_[arr_.index(i)-1] = alt_pos_[i][0]
                            b=0
                        elif arr_[arr_.index(i)-1] == alt_pos_[i][0]:
                            pass
                        else:
                            error = 1
                    else:
                        error = 1
                            
        if alt_pos_[i][1] != '_':
            if alt_pos_[i][1] in arr_:
                if i in arr_:
                    if arr_.index(i) + 1 < len(arr_):
                        if arr_[arr_.index(i)+1] == '_':
                            arr_[arr_.index(i)+1] = alt_pos_[i][1]
                            b=0
                        elif arr_[arr_.index(i)+1] == alt_pos_[i][1]:
                            pass
                        else:
                            error = 1
                    else:
                        error = 1
                elif i not in arr_:
                    if arr_.index(alt_pos_[i][1])-1 >=0:
                        if arr_[arr_.index(alt_pos_[i][1])-1] != '_':
                            pass
                        else:
                            arr_[arr_.index(alt_pos_[i][1])-1] = i
                            b=0
                    else:
                        error = 1
            elif alt_pos_[i][1] not in arr_:
                if i in arr_:
                    if arr_.index(i) + 1 < len(arr_):
                        if arr_[arr_.index(i)+1] == '_':
                            arr_[arr_.index(i)+1] = alt_pos_[i][1]
                            b=0
                        elif arr_[arr_.index(i)+1] == alt_pos_[i][1]:
                            pass
                        else:
                            error = 1
                    else:
                        error = 1
    return arr_,alt_pos_,error,b
