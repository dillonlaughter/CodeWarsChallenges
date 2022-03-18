import itertools
perms = list(map(''.join,sorted(set(list(itertools.permutations(list('ABCDEFGHI')))))))
def count_patterns_from(firstPoint, length):
    if length>9 or length <1:return 0
    global perms
    new_perms = []
    for i in perms:
        if i[0] == firstPoint:
            maybe = []
            for j in ['ABC','CBA','DEF','FED','GHI','IHG','ADG','GDA','BEH','HEB','CFI','IFC','AEI','IEA','CEG','GEC']:
                if j[0]+j[-1] in i:
                    if i.index(j[1]) > i.index(j[0]):
                        maybe.append(False)
            if maybe.count(False)==0:
                new_perms.append(i[0:length])
    return len(set(new_perms))
