import re

def tokenize(expression):
    if expression == "":
        return []
    regex = re.compile("\s*(=>|[-+*\/\%=\(\)]|[A-Za-z_][A-Za-z0-9_]*|[0-9]*\.?[0-9]+)\s*")
    tokens = regex.findall(expression)
    return [s for s in tokens if not s.isspace()]

class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}

    def input(self, expression):
        print(expression)
        tokens = tokenize(expression)
        if tokens == []:
            return ''
        if tokens[0] == 'fn':
            self.fnrunner(tokens)
            return ''
        else:
            fin = self.runner(tokens)
        if type(fin) == type([]):
            if len(fin)>1:raiseE(1)
            return int(fin[0])
        else:return int(fin)

    def fnrunner(self,arr):
        #error checking
        for i in arr[2:arr.index('=>')]:
            if i not in re.sub('[0-9]+|\/|\+|\-|\*|\%|\(|\)|\'|\[|\]|\,|\ ','',str(arr[arr.index('=>')+1:])):
                raiseE(1)
        if len(arr[2:arr.index('=>')]) != len(list(set(arr[2:arr.index('=>')]))):
            raiseE(1)
        if arr[1] in self.vars:
            raiseE(1)

        self.functions[arr[1]] = [arr[arr.index('=>')+1:],arr[2:arr.index('=>')]]
        
    def runner(self,arr):
        if len(arr)> 2:
            if arr[1] == '=' and arr[0] in self.functions:raiseE(1)
        for ind in range(len(arr)-1,-1,-1):
            if len(arr)> ind:
                if arr[ind] in self.functions:
                    temp = self.functions[arr[ind]][0]
                    temp_ind = 0
                    for i in arr[ind+1:ind+1+len(self.functions[arr[ind]][1])]:
                        temp = [i if x == self.functions[arr[ind]][1][temp_ind] else x for x in temp]
                        temp_ind +=1
                    if re.sub('[0-9]+|\/|\+|\-|\*|\%|\(|\)|\'|\[|\]|\,|\ ','',str(temp)) != '':
                        raiseE(1)
                    for k in arr[ind:ind+len(self.functions[arr[ind]][1])+1]:
                        arr.pop(ind)
                    arr.insert(ind,'(')
                    for i in range(len(temp)):
                        arr.insert(ind+i+1,temp[i])
                    arr.insert(ind+i+2,')')
                while '(' in arr or ')' in arr:
                    stack = []
                    ind = 0
                    for i in range(len(arr)):
                        if arr[i] == '(':
                            if ind == 0:
                                stack.append(i)
                            ind+=1
                        if arr[i] == ')':
                            ind-=1
                            if ind == 0:
                                stack.append(i)
                                temp = self.runner(arr[stack[0]+1:stack[1]])
                                for k in range(stack[0],stack[1]+1):
                                    arr.pop(stack[0])
                                temp = self.eva(temp)
                                if type(temp) == type([]):temp = temp[0]
                                arr.insert(stack[0],temp)
                                break
        if len(arr) > 1:
            if arr[1] == '=':
                if arr[0] in self.functions:
                    raiseE()
                self.vars[arr[0]] = self.eva(arr[2:])[0]
                arr = self.vars[arr[0]]
            else:
                arr = self.eva(arr)
        else:
            if arr[0] in self.vars:
                arr = self.vars[arr[0]]
            else:
                raiseE()
        return arr

    def eva(self,arr):
        if len(arr)>2:
            if arr[1] == '=':
                if arr[0] in self.functions:raiseE(1)
                temp = self.eva(arr[2:])
                self.vars[arr[0]] = temp
                arr = temp
        while '*' in arr or '/' in arr or '%' in arr:
            for i in arr:
                if i in ['*','/','%']:
                    arr = self.eva2(arr,i)
                    break
        while '+' in arr or '-' in arr:
            for i in arr:
                if i in ['+','-']:
                    arr = self.eva2(arr,i)
                    break       
        return arr
    
    def eva2(self,arr,i):
        ind = arr.index(i)
        if arr[ind-1] in self.vars:
            arr[ind-1] = self.vars[arr[ind-1]]
        if arr[ind+1] in self.vars:
            arr[ind+1] = self.vars[arr[ind+1]]
        match arr[ind]:
            case '-':
                arr[ind-1:ind+2] = [int(arr[ind-1])-int(arr[ind+1])]
            case '+':
                arr[ind-1:ind+2] = [int(arr[ind-1])+int(arr[ind+1])]
            case '*':
                arr[ind-1:ind+2] = [int(arr[ind-1])*int(arr[ind+1])]
            case '/':
                arr[ind-1:ind+2] = [int(arr[ind-1])/int(arr[ind+1])]
            case '%':
                arr[ind-1:ind+2] = [int(arr[ind-1])%int(arr[ind+1])]
        return arr

def raiseE(x=0):
    if x==0:
        try:raise ValueError('')
        except:pass
    else:
        raise ValueError('')
