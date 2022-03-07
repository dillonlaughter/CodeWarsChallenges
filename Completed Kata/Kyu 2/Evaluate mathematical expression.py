import re
#import string
def calc(string1):
    print(string1)
    string1 = string1.replace(' ','')
    dictionary = {}
    #alpha = list(string.ascii_lowercase)
    alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']   
    
    alpha_ = 0
    while re.search('[0-9]+',string1):
        p = re.search('[0-9]+',string1).group()
        sci = "{:.9e}".format(float(p))
        dictionary[alpha[alpha_]] = sci
        
        string1 = re.sub('[0-9]+',alpha[alpha_],string1,1)
       
        alpha_ +=1
    #print(dictionary)

    string1 = string1.replace('--','+')
    depth = 0
    odepth = 0
    arr = []
    arrpos = 0
    arrindex = 0
    arr,arrindex = runner(string1,arrpos,arrindex)
    while any('(' in k for k in arr): 
        
        for i in range(len(arr)):
            if '(' in arr[i]:
                tarr,arrindex = runner(arr[i],0,arrindex)
                arr[i] = tarr[0]
                for j in tarr[1:]:
                    arr.append(j)
                
                break
        
    #print(arr,dictionary)     
    calcu(arr,dictionary,alpha,alpha_)
    #print(arr[0])
    tempreturn = arr[0]+'&'
    if '.0&' in tempreturn:
        return int(float(arr[0]))
    else:
        return float(arr[0])

def calcu(arr,dictionary,alpha,alpha_):
    add = '(\-)?[0-9]\.[0-9]+[e]((?:\-)?)((?:\+)?)[0-9]+\+(\-)?[0-9]\.[0-9]+[e]((?:\-)?)((?:\+)?)[0-9]+'
    sub = '(\-)?[0-9]\.[0-9]+[e]((?:\-)?)((?:\+)?)[0-9]+\-(\-)?[0-9]\.[0-9]+[e]((?:\-)?)((?:\+)?)[0-9]+'
    mul = '(\-)?[0-9]\.[0-9]+[e]((?:\-)?)((?:\+)?)[0-9]+\*(\-)?[0-9]\.[0-9]+[e]((?:\-)?)((?:\+)?)[0-9]+'
    div = '(\-)?[0-9]\.[0-9]+[e]((?:\-)?)((?:\+)?)[0-9]+\/(\-)?[0-9]\.[0-9]+[e]((?:\-)?)((?:\+)?)[0-9]+'
    while True:
        for i in range(len(arr)):
            arr[i] = arr[i].replace('--','+')
            arr[i] = arr[i].replace('+-','-')
            arr[i] = arr[i].replace('/+','/')
            arr[i] = arr[i].replace('*+','*')
            arr[i] = arr[i].replace('-+','-')
            arr[i] = arr[i].replace('++','+')
        try:
            if all('&' in arr[x] for x in range(1,len(arr))):
                arr[0] = arr[0].replace('--','')
                int(arr[0])
                break
        except:
            try:
                int(round(float(arr[0]),0))
                if all('&' in arr[x] for x in range(1,len(arr))):                    
                    arr[0] = arr[0].replace('--','')
                    int(round(float(arr[0]),0))
                    break
            except:
                pass
            pass
        for i in range(len(arr)):
            if not re.search('[0-9]',arr[i]) and '&' not in arr[i]:
                tempstr = ''
                for j in range(len(arr[i])):
                    try:
                        tempstr = tempstr+dictionary[arr[i][j]]
                    except:
                        tempstr = tempstr+arr[i][j]
                while any(z in tempstr for z in ['--','+-','/+','*+','++','-+']):
                    tempstr = tempstr.replace('--','+')
                    tempstr = tempstr.replace('+-','-')
                    tempstr = tempstr.replace('/+','/')
                    tempstr = tempstr.replace('*+','*')
                    tempstr = tempstr.replace('++','+')
                    tempstr = tempstr.replace('-+','-') 
                tempstr = tempstr.replace('--','+')
                #replace d neg to pos
                while any(k in tempstr for k in ['*','/']) or re.search('[0-9]\-[0-9]|[0-9]\+[0-9]',tempstr):
                    while any(z in tempstr for z in ['--','+-','/+','*+','++','-+']):
                        tempstr = tempstr.replace('--','+')
                        tempstr = tempstr.replace('+-','-')
                        tempstr = tempstr.replace('/+','/')
                        tempstr = tempstr.replace('*+','*')
                        tempstr = tempstr.replace('++','+')
                        tempstr = tempstr.replace('-+','-') 
                   
                    try:
                        if tempstr.index('+') == 0:
                        
                            tempstr = tempstr.replace('+','',1)
                    except:
                        pass
                    if '*' in tempstr or '/' in tempstr:
                        try:
                            p1 = tempstr.index('/')
                            p2 = tempstr.index('*')
                            if p1<p2:
                                sign = 'div'
                            else:
                                sign = 'mul'
                            if sign == 'div':
                                p =re.search(div,tempstr).group()
                                placeholder = p.index('/')
                                ev = float(p[0:placeholder])/float(p[placeholder+1:])
                                ev = '{:.9e}'.format(float(ev))
                                tempstr = re.sub(div,'+'+str(ev),tempstr,1)
                            if sign == 'mul':
                                p =re.search(mul,tempstr).group()
                                placeholder = p.index('*')
                                ev = float(p[0:placeholder])*float(p[placeholder+1:])
                                ev = '{:.9e}'.format(float(ev))
                                tempstr = re.sub(mul,'+'+str(ev),tempstr,1)
                        except:
                            if '*' in tempstr:
                                p =re.search(mul,tempstr).group()
                                placeholder = p.index('*')
                                ev = float(p[0:placeholder])*float(p[placeholder+1:])
                                ev = '{:.9e}'.format(float(ev))
                                tempstr = re.sub(mul,'+'+str(ev),tempstr,1)
                            elif '/' in tempstr:
                                p =re.search(div,tempstr).group()
                                placeholder = p.index('/')
                                ev = float(p[0:placeholder])/float(p[placeholder+1:])
                                ev = '{:.9e}'.format(float(ev))
                                tempstr = re.sub(div,'+'+str(ev),tempstr,1)
                    elif '+' in tempstr or '-' in tempstr:
                        try:
                            x=0
                            y=0
                            varerr = 0
                            while varerr != 2:
                                varerr = 0
                                p1 = tempstr.index('+',x)
                                if tempstr[p1-1] == 'e':
                                    x=p1+1
                                    
                                else:
                                    varerr+=1
                                p2 = tempstr.index('-',y)
                                if tempstr[p2-1] == 'e' or p2 == 0:
                                    y=p2+1
                                    
                                else:
                                    varerr+=1
                            if p1<p2:
                                sign = 'add'
                            else:
                                sign = 'sub'
                            if sign == 'add':
                                p =re.search(add,tempstr).group()
                                placeholder = p.index('+',x)
                                ev = float(p[0:placeholder])+float(p[placeholder+1:])
                                ev = '{:.9e}'.format(float(ev))
                                tempstr = re.sub(add,str(ev),tempstr,1)
                            if sign == 'sub':
                                try:
                                    p =re.search(sub,tempstr).group()
                                    placeholder = p.index('-',y)
                                    if placeholder == 0:
                                        placeholder = p.index('-',1)
                                    ev = float(p[0:placeholder])-float(p[placeholder+1:])
                                    ev = '{:.9e}'.format(float(ev))
                                    tempstr = re.sub(sub,str(ev),tempstr,1)
                                except:
                                    try:
                                        p = re.search(add,tempstr).group()
                                        placeholder = p.index('+',x)
                                        ev = float(p[0:placeholder])+float(p[placeholder+1:])
                                        ev = '{:.9e}'.format(float(ev))
                                        tempstr = re.sub(add,str(ev),tempstr,1)
                                    except:
                                        pass
                        except:
                            if '-' in tempstr:
                                try:
                                    x=0
                                    y=0
                                    varerr = 0
                                    while varerr != 1:
                                        varerr = 0
                                        p1 = tempstr.index('-',x)
                                        if tempstr[p1-1] == 'e' or p1 == 0:
                                            x=p1+1
                                            
                                        else:
                                            varerr+=1
                                    try:
                                        p =re.search(sub,tempstr).group()
                                        placeholder = p.index('-',x)
                                        if placeholder == 0:
                                            placeholder = p.index('-',1)
                                        ev = float(p[0:placeholder])-float(p[placeholder+1:])
                                        ev = '{:.9e}'.format(float(ev))
                                        tempstr = re.sub(sub,str(ev),tempstr,1)
                                    except:
                                        try:
                                            p = re.search(add,tempstr).group()
                                            placeholder = p.index('+',x)
                                            ev = float(p[0:placeholder])+float(p[placeholder+1:])
                                            ev = '{:.9e}'.format(float(ev))
                                            tempstr = re.sub(add,str(ev),tempstr,1)
                                        except:
                                            pass
                                except:
                                    pass
                            if '+' in tempstr:
                                try:
                                    x=0
                                    y=0
                                    varerr = 0
                                    while varerr != 1:
                                        varerr = 0
                                        p1 = tempstr.index('+',x)
                                        if tempstr[p1-1] == 'e':
                                            x=p1+1
                                            
                                        else:
                                            varerr+=1
                                    p =re.search(add,tempstr).group()
                                    placeholder = p.index('+',x)
                                    ev = float(p[0:placeholder])+float(p[placeholder+1:])
                                    ev = '{:.9e}'.format(float(ev))
                                    tempstr = re.sub(add,str(ev),tempstr,1)
                                except:
                                    pass
                    while any(z in tempstr for z in ['--','+-','/+','*+','++','-+']):
                        tempstr = tempstr.replace('--','+')
                        tempstr = tempstr.replace('+-','-')
                        tempstr = tempstr.replace('/+','/')
                        tempstr = tempstr.replace('*+','*')
                        tempstr = tempstr.replace('++','+')
                        tempstr = tempstr.replace('-+','-')                                
                dictionary[alpha[alpha_]] = tempstr
                if i!=0:
                    arr[i] = '&'
                    for j in range(len(arr)):
                        arr[j] = arr[j].replace(str(i),alpha[alpha_])
                    alpha_+=1
                else:
                    arr[0] = tempstr
    return arr
                
def runner(string1,arrpos,arrindex):
    arr = ['']
    for i in range(len(string1)):
        if string1[i] == '(':
            depth =1
            temppos = 0
            arrindex +=1
            forj = string1[i+1:]
            for j in range(len(string1[i+1:])):
                if string1[i+j+1] == '(':
                    depth +=1
                if string1[i+j+1] == ')':
                    if depth != 0:
                        depth -= 1
                    if depth == 0:
                        append = string1[i+1:temppos+i+1]
                        break
                temppos+=1
            arr.append(append)
            arr[arrpos] = arr[arrpos]+str(arrindex)+string1[temppos+i+2:]
            break
        arr[arrpos] = arr[arrpos]+string1[i]
    return arr,arrindex
