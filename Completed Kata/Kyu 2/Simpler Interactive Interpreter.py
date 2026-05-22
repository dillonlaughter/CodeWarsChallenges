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
        tokens = tokenize(expression)
        if tokens == []:
            return ''
        fin = self.runner(tokens)
        if type(fin) == type([]):
            if len(fin)>1:raiseE(1)
            return int(fin[0])
        else:return int(fin)
        
    def runner(self,arr,x=0):
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
                        arr[stack[0]:stack[1]+1] = self.eva(temp)
                        break
        if len(arr) > 1:
            if arr[1] == '=':
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
