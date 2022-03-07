def decodeBitsAdvanced(bits):
    return bits
        
dict = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ',':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-','':'',
                    'SOS':'...---...','!':'-.-.--',' ':'   '}
def decodeMorse(bits):
    try:
        while bits[0] != '1':
            bits = bits[1:]
    except:
        pass
    try:
        while bits[-1] != '1':
            bits = bits[:-1]
    except:
        pass
    if bits == '' or bits.count('1') == 0:
        return ''
    for i in range(1,10):
        if bits.count('0') == 0:
            return 'E'
    
    bits += '0'
    zero = 0
    ones = 0
    space = 0
    word = 0
    dash = 0
    arr1 = []
    arr2 = []
    while True:## change for smaller strings
        try:
            j=0
            zero = 0
            if bits[0] == '0':
                while bits[j] == '0':
                    j+=1
                    zero +=1
                bits = bits[j:]
                arr1.append('0')
                arr2.append(str(zero))
            j=0
            zero=0
            if bits[0] == '1':
                while bits[j] == '1':
                    j+=1
                    zero +=1
                bits = bits[j:]
                arr1.append('1')
                arr2.append(str(zero))
        except:
            print(arr1 , 'arr1')
            print(arr2 , 'arr2')
            break    
    morse = []
    ones = []
    for i in range(len(arr1)):
        if int(arr1[i]) == 1:
            ones.append(int(arr2[i]))
        #get a list (ones) of the quantities of ones
    max1 = max(ones)
    min1 = min(ones)
    zeroes = []
    for i in range(len(arr1)):
        if int(arr1[i]) == 0:
            zeroes.append(int(arr2[i]))
        #get a list (ones) of the quantities of ones
    max0 = max(zeroes)
    min0 = min(zeroes)
    for index in range(len(arr1)):
        replace0 = {1:[2,2],2:[3,2],3:[4,3],4:[4,4],5:[4,3],6:[4,3],7:[4,3],8:[5,3],9:[4,3],10:[6,3],11:[6,4]}
        replace1 = {1:[1],2:[1],3:[3],4:[4],5:[4],6:[3],7:[3],8:[4]}

        if min0 < max0:
            if max0 < 17 and max0 != 28:
                replace0new = [(max0+min0)//2,(max0+min0)//3]
            elif max0 == 28:
                replace0new = [(max0+min0)//2+1,(max0+min0)//3-1]
            else:
                replace0new = [(max0+min0)//2,(max0+min0)//3-1]
        else:
            if min1 > min0:
                replace0new = [min0+1,min0+1]#replace0new = [(max0+min0)/2,(max0+min0)/3]
            elif min1 == min0:
                replace0new = [max0+1,min0+1]
            else:
                if max0 > 4*min([min1,min0]):
                    replace0new = [(max0)/2,(max0)/3]
                else:
                    replace0new = [max0+1,max0]


        if min1 < max1:
            if max1 < 8 and max1 != 14:
                replace1new = (max1+min1)/2
            elif max1 == 14:
                replace1new = (max1+min1)/2
            else:
                replace1new = (max1+min1)/2-1
        else:
            if min0 >= min1:
                replace1new = (max1+min1)/2
            else:
                replace1new = max1-1

        if int(arr1[index]) == 0:
            if int(arr2[index]) > replace0new[0] and int(arr2[index]) != 10:
                morse.append('   ')
            if int(arr2[index]) >= replace0new[1] and int(arr2[index]) <replace0new[0]+1:
                morse.append(' ')
            if int(arr2[index]) == 10 and max0 == 18:
                morse.append(' ')
            
        if int(arr1[index]) == 1:
            if int(arr2[index]) > replace1new:
                morse.append('-')
            if int(arr2[index]) <= replace1new:
                morse.append('.')
    while True:
        if ' ' in morse[0]:
            morse = morse[1:]
        if ' ' in morse[-1]:
            morse = morse[:-1]
        break
    return decodeMorseOrig(''.join(morse))
    
def decodeMorseOrig(message):
    message += ' '
    decipher = ''
    citext = ''
    i=0
    for letter in message:
        if letter != ' ':
            i = 0
            citext += letter
        else:
            i += 1
            if i == 2 :
                decipher += ' '
            else:
                decipher += list(dict.keys())[list(dict.values()).index(citext)]
                citext = ''
    if decipher[0] == ' ':
        decipher = decipher[1:]
    if decipher[-1] == ' ':
        decipher = decipher[:-1]
    try:
        decipher=decipher.replace('W E','WE')
    except:
        pass
    print('decipher '+decipher)
    return decipher
