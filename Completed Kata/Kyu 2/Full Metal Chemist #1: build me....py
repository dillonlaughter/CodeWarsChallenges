import re
class Atom(object):
    
    def __init__ (self, elt, id_):
        
        self.element = elt
        self.id = id_
        self.id_ = id_
        self.sides = []
        self.branch = -10
        self.H = 0
        self.priority = -1
        self.old_branch = -10

        self.name = 'Atom('+self.element+'.'+str(self.id_)+')'

    def update(self):
        self.name = 'Atom('+self.element+'.'+str(self.id_)
        temp = []
        
        self.sides = sorted(self.sides,key = lambda x: (x.H,x.priority,x.element,x.id_))
        for i in self.sides:
            if i.element != 'H':
                temp.append(i.element+str(i.id_))
            else:
                temp.append(i.element)
        temp = ','.join(temp)
        
        if temp == '':self.name +=')'
        else:self.name += ': '+temp+')'

            
        
        #sorting
        
    def __hash__(self):      return self.id
    def __eq__(self, other): return self.id == other.id

    def __str__(self):
        return self.name
    
data = {'H':[1,1.0,2],
        'B':[3,10.8,4],
        'C':[4,12.0,1],
        'N':[3,14.0,4],
        'O':[2,16.0,3],
        'F':[1,19.0,4],
        'Mg':[2,24.3,4],
        'P':[3,31.0,4],
        'S':[2,32.1,4],
        'Cl':[1,35.5,4],
        'Br':[1,80.0,4]    
}    
    
class Molecule(object):
    def __init__(self,name = ''):
        print('oc = Molecule()')
        
        self.atoms = []
        self.brances = 0
        self.name = name
        self.locked = False

    def __setitem__(self,*args,**kwargs):
        if self.locked == True:
            raise LockedMolecule
    
    def __getattr__(self,name):
        if name in self.__dict__.keys():
            return self.__dict__.values()[name]
        else:
            raise UnlockedMolecule
        
    def get_formula(self):
        self.__dict__['formula'] = None
        temp = []
        temp = sorted(self.atoms, key =lambda x: (x.priority, x.element))
        temp = [x.element for x in temp]
        temp2 = ''
        
        while len(temp)>=1:
            temp2 += temp[0]
            var = str(temp.count(temp[0]))
            if var != '1':
                temp2+=var
            temp = temp[int(var):]        
        
        self.formula = temp2
        return self
            
    def get_mol_weight(self):
        self.__dict__['molecular_weight'] = 0
        for i in self.atoms:
            self.molecular_weight+=data[i.element][1]
        return self
            
        
    def brancher(self, *args):
        print('oc.brancher',args)
        if self.locked == True:raise LockedMolecule
        id_ = 1
        max_branch = 0
        max_id_ = 0
        for i in self.atoms:
            if i.branch > max_branch:
                max_branch = i.branch
            if i.id_ >= max_id_:
                max_id_ = i.id_
        id2_ = max_branch+1
        id_1 = max_id_
        for k in range(len(args)):
            for i in range(args[k]): #each branch in linked list
                if i == 0:
                    temp = Atom('C',i+id_)
                    temp.branch = k +id2_
                    temp.id_ = i+id_+id_1 
                    temp.priority = data[temp.element][2]
                    self.atoms.append(temp)
                else:
                    temp = Atom('C',i+id_)
                    temp.branch = k+id2_
                    temp.id_ = i+id_+id_1
                    temp.priority = data[temp.element][2]
                    self.atoms[-1].sides.append(temp)
                    temp.sides.append(self.atoms[-1])
                    self.atoms.append(temp)
            id_1+=args[k]
        for i in self.atoms:i.update()
            
        return self

    def printer(self):
        arr = []
        temp = ''
        for i in self.atoms:
            if i.element == 'H':
                continue
            temp+= i.element +' '+ str(i.id)+'  '
            for j in i.sides:
                temp+= j.element+' '+str(j.id)+'    '
            temp+='\n\n-------\n'
        arr.append(temp)
        for i in arr:
            print(i)
            
    def bounder(self, *args):
        print('oc.bounder',args)
        for k in args:
            self.bounder_(k)
        return self
            
    def bounder_(self, *args):
        print('bounder_',args)
        if self.locked == True:raise LockedMolecule
        for k in range(len(args)):
            c1,b1,c2,b2 = args[k]
            if c1 == c2 and b1 == b2:raise InvalidBond
            c1id = None
            c2id = None
            
            for i in self.atoms:
                if i.id == c1 and i.branch == b1:
                    c1id = i
                if i.id == c2 and i.branch == b2:
                    c2id = i
            if not c1id:
                raise InvalidBond
            if not c2id:
                raise InvalidBond    
            
            if len(c1id.sides) >= data[c1id.element][0]:
                raise InvalidBond
                
            if len(c2id.sides) >= data[c2id.element][0]:
                raise InvalidBond
                
            c1id.sides.append(c2id)
            c2id.sides.append(c1id)
        for i in self.atoms:i.update() 

        return self
    
    def mutate(self,*args):
        print('oc.mutate',args)
        if self.locked == True:raise LockedMolecule
        for k in range(len(args)):
            nc,nb,elt = args[k]
            for i in self.atoms:
                if i.id == nc and i.branch == nb:
                    if len(i.sides) > data[elt][0]:raise InvalidBond
                    i.element = elt
                    i.priority = data[i.element][2]
                    if i.element =='H':i.H=1
                    else:i.H=0
                for z in self.atoms:z.update()
        return self
    
    def add(self,*args):
        print('oc.add',args)
        if self.locked == True:raise LockedMolecule
        for k in range(len(args)):
            nc,nb,elt = args[k]
            for i in self.atoms:
                if i.id == nc and i.branch == nb:
                    maxid = 0
                    for z in self.atoms:
                        if z.branch == i.branch:
                            if z.id > maxid:
                                maxid = z.id
                    
                    temp = Atom(elt,maxid+1)
                    temp.branch = nb
                    temp.id_ = len(self.atoms)+1
                    temp.priority = data[temp.element][2]
                    if temp.element =='H':temp.H=1
                    try:
                        if len(temp.sides) >= data[temp.element][0]:raise InvalidBond
                        
                        temp.sides.append(i)
                        if len(i.sides) >= data[i.element][0]:raise InvalidBond
                        
                        i.sides.append(temp)
                        self.atoms.append(temp)
                    except InvalidBond:
                        for z in self.atoms:z.update()
                        raise InvalidBond
                    for z in self.atoms:z.update()
                    
            for z in self.atoms:z.update()
        for z in self.atoms:z.update()
        return self
    
    def add_chaining(self,nc,nb,*args):
        print('oc.add_chaining(',nc,',',nb,',',args,')')
        if self.locked == True:raise LockedMolecule
        for i in ['F','H','Cl','Br']: 
            if i in args[0:-1]:
                raise InvalidBond
        for k in range(len(args)):
            elt = args[k]
            if k == 0:
                self.add((nc,nb,elt))         
            else:       
                self.add((self.atoms[-1].id,nb,elt))
        for z in self.atoms:z.update()
        return self
        
    def closer(self):
        print('oc.closer()')
        if self.locked == True:raise LockedMolecule
        if len(self.atoms) == 1:
            for _ in range(data[self.atoms[0].element][0]):
                temp = Atom('H',len(self.atoms)+1)
                temp.priority = data[temp.element][2]
                self.atoms[0].sides.append(temp)
                temp.sides.append(self.atoms[0])
                self.atoms.append(temp)
        else:
            for j in range(len(self.atoms)):
                i = self.atoms[j]
                
                for k in range(data[i.element][0]):
                    try:
                        _ = i.sides[k]
                    except:
                        temp = Atom('H',len(self.atoms)+1)
                        temp.priority = data[temp.element][2]
                        i.sides.append(temp)
                        temp.sides.append(i)
                        self.atoms.append(temp)
                
        for i in self.atoms:
            if i.element == 'H':
                i.H = 1
            
        for i in self.atoms:
            i.update()
            
        #formula
        self.get_formula()

        #weight
        self.get_mol_weight()

        self.locked = True
        return self
        
    
    def unlock(self):
        print('oc.unlock()')
        self.locked = False
        del self.formula
        del self.molecular_weight
        
        #remove hydrogens
        for i in range(len(self.atoms)-1,-1,-1):
            for j in range(len(self.atoms[i].sides)-1,-1,-1):
                if self.atoms[i].sides[j].element == 'H':
                    self.atoms[i].sides.pop(j)
            if self.atoms[i].element == 'H':
                self.atoms.pop(i)
        

        #remove empty branches
        arr = {}
        max_branch = -1
        for i in range(len(self.atoms)):
            self.atoms[i].id_ = i+1
            if self.atoms[i].branch not in arr:
                arr[self.atoms[i].branch] = []
            arr[self.atoms[i].branch].append(self.atoms[i])
        
        for branch in arr:
            for atom in range(len(arr[branch])):
                arr[branch][atom].id = atom+1
                arr[branch][atom].branch = list(arr.keys()).index(branch)+1
        
        #if all empty branches, throw EmptyMolecule exception
        if len(self.atoms) == 0:raise EmptyMolecule
            
        for i in self.atoms:i.update()
        return self

    def bonds(self):
        for i in self.atoms:
            if i.element != 'H':
                print(i.name)
        return self
    
def check(s,oc=None):
    import ast
    a,b = s.split(' should equal')
    a=ast.literal_eval(a.replace('"',''))
    b=ast.literal_eval(b.replace('"',''))
    if oc==None:
        for i in range(len(b)):
            print(a[i])
            print(b[i])
            print('')
    else:
        arr = []
        for i in oc.atoms:
            if i.element != 'H':
                arr.append(i.name)

        for i in range(max(len(b),len(a),len(arr))):
            if 1==1:
                try:print('here', arr[i])
                except:pass
                try:print('code',a[i])
                except:pass
                try:print('expt',b[i])
                except:pass
                print('')

class InvalidBond(Exception):
    def __init__(self):
        print(Exception)
        return
        
class UnlockedMolecule(Exception):
    def __init__(self):
        print(Exception)
        return
    
class LockedMolecule(Exception):
    def __init__(self):
        print(Exception)
        return
        
class EmptyMolecule(Exception):
    def __init__(self):
        print(Exception)
        return
