import itertools
from math import factorial
def listPosition(word):
    #works but too slow
    #return 1+list(map(''.join,sorted(set(list(itertools.permutations(list(word))))))).index(word)

    word = list(word)
    print(word)
    s = sorted(word)
    sum_ = 0
    if len(set(word)) == len(word):
        sum_=0
        while len(word)>0:
            pos_change = s.index(word[0])
            new_pos = len(word)-1
            a= factorial(new_pos)*pos_change
            sum_+=a
            s.remove(word[0])
            word.remove(word[0])
        sum_+=1
    else:
        while len(word)>1:
            fact = factorial(len(word))
            for i in set(word):
                fact = fact//factorial(word.count(i))
            for i in set(word):
                if i < word[0]:
                    sum_ += fact//len(word)*word.count(i)
            word = word[1:]
        sum_ = sum_//1+1
        
    return sum_
