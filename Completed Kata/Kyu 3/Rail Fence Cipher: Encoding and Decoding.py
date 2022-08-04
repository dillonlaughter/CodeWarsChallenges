from itertools import zip_longest

def encode_rail_fence_cipher(string, n,temp=0):
    arr = [[] for i in range(n)]
    cur_rail = 0
    direction = 'down'
    for i in string:
        if direction == 'down':
            if cur_rail < n-1:
                arr[cur_rail].append(i)
                cur_rail +=1
                continue
            if cur_rail == n-1:
                direction = 'up'
                arr[cur_rail].append(i)
                cur_rail -=1
                continue
        if direction == 'up':
            if cur_rail >0:
                arr[cur_rail].append(i)
                cur_rail-=1
                continue
            if cur_rail == 0:
                direction = 'down'
                arr[cur_rail].append(i)
                cur_rail +=1
                continue
    if temp == 0:
        return ''.join([''.join(arr[i]) for i in range(len(arr))])
    else:
        return arr
    
def show(string,n):
    string = string+' '*(n-len(string)%n)
    str1 = [string[i:i+n] for i in range(0,len(string),n)]
    for i in range(len(str1)):
        str1[i] = list(str1[i])
    for i in range(len(str1)):
        for j in range(len(str1[i]),0,-1):
            str1[i].insert(j-1,' '*j)
        str1[i] = [str1[i][k:k+2] for k in range(0,len(str1[i]),2)]
        str1[i] = [''.join(str1[i][j]) for j in range(len(str1[i]))]
        if i%2 == 1:
            str1[i] = str1[i][::-1]
    a = transpose(str1)
    for i in a:print(i)

def transpose(list_of_lists):
    tranposed_tuples = zip_longest(*list_of_lists, fillvalue=None)
    transposed_tuples_list = list(tranposed_tuples)
    a= (list(transposed_tuples_list))
    for i in range(len(a)):
        a[i] = list(a[i])
    return a

def decode_rail_fence_cipher(string, n):
    if string == '':return ''
    repl = []
    doit = 0
    if ' ' in string:
        if '@' not in string:
            doit = 1
            
        repl.append(' ')
    else: repl.append('|')
    if '@' not in string:
        repl.append('@')
    if doit ==1:
        string = string.replace(' ','@')

    arr = [[] for i in range(n+n-2)]
    cur_rail = 0
    for i in range(len(string)):
        arr[i%(n+n-2)].append(string[i])
    temp = []
    arr1 = transpose(arr)
    
    for i in range(len(arr1)):
        for j in range(arr1[i].count(None)):
            arr1[i].pop()
    str1 = ''.join(''.join(arr1[i]) for i in range(len(arr1)))
    arr1 = encode_rail_fence_cipher(string,n,1)
    arr2 = []

    while True:
        try:
            arr2.append(list(str1[0:len(arr1[0])]))
            str1 = str1[len(arr1[0]):]
            arr1.pop(0)
        except:
            break
    temp = [arr2[-1],[' ' for i in range(len(arr2[-1]))]]

    temp = transpose(temp)

    arr2[-1] = list(''.join(''.join(temp[i]) for i in range(len(temp))))
    arr2[-1].pop()

    for i in range(2,1+len(arr2[0])):
        arr2[0].insert(i,' ')
        
    temp1 = 2 
    for i in range(len(arr2[0])//2+1,len(arr2[0])-1,1):
        arr2[0][i],arr2[0][temp1] = arr2[0][temp1],arr2[0][i]
        temp1+=2
    
    
    arr3 = transpose(arr2)
    
    for i in range(len(arr3)):
        if i%2==1:
            arr3[i] = arr3[i][::-1]
    for i in range(len(arr3)):
        while None in arr3[i]:
            arr3[i].remove(None)
    res = ''.join(''.join(arr3[i]) for i in range(len(arr3)))
    res = res.replace(' ','')
    res = res.replace(repl[1],repl[0])
    show(res,n)
    return res
