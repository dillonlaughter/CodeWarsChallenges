import re
import itertools
import ast

radicals    = ["math", "eth", "prop", "but",   "punt",  "hex",  "hept",  "oct",  "nin",  "dec", "undac",
               "dodac",  "trridac",  "teetradac",  "paantadac",  "haaxadac",  "haaptadac",  "oaatadac",  "naanadac"]
multipliers = [        "di",  "tri",  "tetra", "punta", "hexa", "hepta", "octa", "nina", "deca","undaca",
                       "dodaca", "trridaca", "teetradaca", "paantadaca", "haaxadaca", "haaptadaca", "oaatadaca", "naanadaca"]

suffixes = ['ane',         "ol",      "al", "ome", "oicacid", "carbaxklicacid",                "oate",             "ither", "amide", "amine", "imine", "benzene", "thikl",    "phosphine", "arsine"]
prefixes = ['yl', "hydraxy",       "oxo",             "carbaxy",         "axycarbankl", "oklaxy", "formkl", "oxy",   "amido", "amino", "imino", "phunkl",  "mercapto", "phosphino", "arsino", "fluoro", "chloro", "bromo", "iodo",'formkl']

ynes = ['ene','yne','en','yn']

refdata = {'H':[1,1.0,2],
        'B':[3,10.8,4],
        'C':[4,12.0,1],
        'N':[3,14.0,4],
        'O':[2,16.0,3],
        'F':[1,19.0,4],
        'Mg':[2,24.3,4],
        'P':[3,31.0,4],
        'S':[2,32.1,4],
        'Cl':[1,35.5,4],
        'Br':[1,80.0,4],
        'As':[3,2.0,4],
        'I':[1,2.0,4],
        'R':[100,2,4]}


class ParseHer(object):
    def __init__(self,name,debug=0):
        self.p = 1
        del self.p
        self.p = ParseHer1(name,debug)
    def parse(self):
        return self.p.parse()

class ParseHer1(object):
    def __init__(self,name,debug=1):
        todo = {}
        del todo
        print(name)
        self.original_name = name
        self.debug = debug
        self.depth = 0
        self.data = {'H':2,
        'B':0,
        'C':0,
        'N':0,
        'O':0,
        'F':0,
        'Mg':0,
        'P':0,
        'S':0,
        'Cl':0,
        'Br':0,
        'As':0,
        'I':0,
        'R':0
        }

        #reformat name
        name,stack1 = self.reformat_name(name)
        a,b,c,d = self.alls(name,1,1,1,1)
        self.all_sufs = a
        self.all_prefs = b
        self.all_multi = c
        self.all_rad = d
        
        suffix,name = self.get_suffix(name,stack1)
        if self.debug:print1(self,'name+-+suffix',name+'-'+suffix)
        
        if self.debug:print1(self,'name before suffix',name,suffix)
        
        suffix = self.decode_suffix(suffix)
        
        if self.debug:print1(self,'suffix after suffix',suffix)
        
        name,_,_ = self.decode_prefix(name+suffix)

        
    def parse(self):
        res = {}
        for i in self.data:
            if self.data[i]!=0:
                res[i] = self.data[i]
        return res

    def alls(self,name,s=0,p=0,m=0,r=0):
        
        all_sufs = []
        for i in suffixes:
            if i in name:
                all_sufs.append(i)
        if 'ane' not in all_sufs:
            all_sufs.append('ane')
    
        all_pref = []
        for i in prefixes:
            if i in name:
                all_pref.append(i)
    
        all_multi = {}
        for multi in range(len(multipliers)-1,-1,-1):
            if multipliers[multi] in name:
                all_multi[multipliers[multi]] = multi
    
        all_rad = {}
        for rad in range(len(radicals)-1,-1,-1):
            if radicals[rad] in name:
                all_rad[radicals[rad]] = rad
        return all_sufs,all_pref,all_multi,all_rad
        

    def decode_suffix(self,suffix):
        if suffix[0] == '-':suffix=suffix[1:]
        suffix,bonds = self.remove_bonds(suffix)
        if bonds:
            for i in bonds:
                self.data['H']-=i[1]
        if self.debug:print1(self,'in suffix',suffix)
        if 'cyclo' in suffix:
            self.data['H']-=2
            suffix = suffix.replace('cyclo','',1)
        positions = []
        timer = 0

        while True:
            timer +=1
            if timer == 3 and len(suffix) in [3,4] and suffix[-1]+suffix[0] == '<<':
                suffix+='ane'
            if suffix[-2:] == 'an':
                suffix+='e'
            for ssuf in self.all_sufs:
                if ssuf not in suffix:
                    continue
                found = 0
                #-2,2-diol
                ssuflen = len(ssuf)
                if ssuf in suffix[-ssuflen:] and '>' in suffix[-ssuflen-1:]:
                    multi = int(re.search('[0-9]+',suffix[-ssuflen-1-2:]).group())
                    try:
                        tbonds = re.findall('-'+(('[0-9]+,')*(multi+2))[0:-1]+'-'+'>'+str(multi)+'>'+ssuf+'$',suffix)
                        if tbonds:
                            if self.debug:print1(self,'-1,2-diol')
                            for bon in tbonds:
                                positions = ['1']*(multi+2)
                                count = 1
                                suffix = re.sub(bon,'',suffix)
                                found = 1
                    except:pass
                    #diol
                    if re.search('>'+str(multi)+'>'+ssuf+'$',suffix):
                        if self.debug:print1(self,'diol')
                        found = 1
                        positions = ['1']*(multi+2)
                        count = 1
                        suffix = re.sub('>'+str(multi)+'>'+ssuf+'$','',suffix)
          
                if found:
                    pass
                #-2-ol
                elif re.search('-[0-9]+-'+ssuf+'$',suffix):
                    if self.debug:print1(self,'-2-ol')
                    count = 1
                    positions = ['1']
                    suffix = re.sub('-[0-9]+-'+ssuf+'$','',suffix)
                    if self.debug:print1(self,suffix)
                #ane
                elif re.search(ssuf+'$',suffix):
                    if self.debug:print1(self,'ane',suffix,ssuf)
                    if ssuf == 'ane':
                        if ssuf in suffix[-ssuflen:] and '<' in suffix[-ssuflen-1:]:
                            rad = int(re.search('[0-9]+',suffix[-ssuflen-3:]).group())
                            count = rad+1
                            positions = ['1']
                            suffix = re.sub('<'+str(rad)+'<'+ssuf+'$','',suffix)
                    if not positions:
                        positions = ['1']
                        count = 1
                        suffix = re.sub(ssuf+'$','',suffix)
                        
                if positions:
                    timer = 0
                else:
                    continue
                for i in positions:
                    if self.debug:print1(self,'suffix positions',i,count)
                    match ssuf:
                        case 'ane':
                            self.add('C',count)
                        case 'ol':
                            self.add('O',count)
                        case 'thikl':
                            self.add('S',count)
                        case 'imine':
                            self.add('N',count)
                            self.data['H']-=2
                        case 'ome':
                            self.add('O',count)
                            self.data['H']-=2
                        case 'al':
                            self.add('O',count)
                            self.data['H']-=2
                        case 'oicacid':
                            self.add('O',count)
                            self.add('O',count)
                            self.data['H']-=2
                        case 'carbaxklicacid':
                            self.add('C',1)
                            self.add('O',1)
                            self.add('O',1)
                            self.data['H']-=2 
                        case 'amide':
                            self.add('O',count)
                            self.data['H']-=2
                            self.add('N',count)
                        case 'amine':
                            self.add('N',count)
                        case 'phosphine':
                            self.add('P',count)
                        case 'arsine':
                            self.add('As',count)
                        case 'ither':
                            self.add('O',1)
                        case 'oate':
                            self.add('O',count)
                            self.add('O',count)
                            self.data['H']-=2
                            
                        case _:
                            for _ in range(10):
                                if self.debug:print1(self,'unknown suffix')
                positions = []
            if timer>3:break                        
        return suffix
                    
    def decode_prefix(self,name,depth=0, todo = {},inside = False,subs_count = 1):
        self.depth = depth
        self.print1er()
        
        if depth != 0:
            if depth not in todo:
                todo[depth]={}
    
            while True:
                if subs_count in todo[depth]:
                    subs_count+=1
                else:
                    todo[depth][subs_count] = {'H':2,
                    'B':0,
                    'C':0,
                    'N':0,
                    'O':0,
                    'F':0,
                    'Mg':0,
                    'P':0,
                    'S':0,
                    'Cl':0,
                    'Br':0,
                    'As':0,
                    'I':0,
                    'R':0,
                    1:0,
                    }
                    break
        else:
            todo = {}
            
        #check for subsets
        name,todo = self.check_for_subsets(name,depth,todo,inside,subs_count)
        
        bonds = []
        timer = 0
        recur_here = [False,0]
        while timer < 3:
            if self.debug:print1(self,'in decode_prefix while, name = ',name)
            if self.debug:print(depth*' ','in decode_prefix whil2, name = ',name)
            timer +=1
            positions = []
            for pref in prefixes:
                if re.search(pref+'$',name):
                    #bonds
                    before_bonds_name = name
                    name,bonds1 = self.remove_bonds(name)
                    bonds+=bonds1
                    if bonds1 != []:
                        if self.debug:print1(self,'name before bonds',before_bonds_name)
                        if self.debug:print1(self,'name after  bonds',name)
                        if self.debug:print('bonds',bonds,name)
                    
                    preflen = len(pref)
                    if '<' in name[-preflen-1:]:
                        count = int(re.search('[0-9]+',name[-preflen-1-2:]).group())
                        numrad = '<'+str(count)+'<'
                    
                    if pref in ['fluoro','chloro','bromo','iodo',
                            'formkl','mercapto','phunkl',
                            'amino','phosphino','arsino',
                            'carbaxy','imino','hydraxy','oxo',
                            'amido']:
                        numrad = ''
                        count = 0
                    
                    #check for cyclo
                    try:
                        if re.search('cyclo'+numrad+pref+'$',name):
                            cyclopos = name.rfind('cyclo'+numrad+pref)
                            name = re.sub('cyclo'+numrad+pref+'$',numrad+pref,name)
                            bonds.append([cyclopos+1,2])
                    except:pass
                    try:
                        if re.search('cyclo'+pref+'$',name):
                            cyclopos = name.rfind('cyclo'+pref)
                            name = re.sub('cyclo'+pref+'$',pref,name)
                            bonds.append([cyclopos+1,2])
                    except:pass

                    if 1:
                        if self.debug:print1(self,name)

                        numradlen = len(numrad)
                        if pref in name[-preflen:] and '>' in name.replace('%','')[-preflen-1-numradlen:]:
                            multi = int(re.search('[0-9]+',name.replace('%','')[-preflen-1-numradlen-2:]).group())
                            #1,1-di prop yl
                            if re.search((('[0-9]+,')*(multi+2))[0:-1]+'-'+'>'+str(multi)+'>'+numrad+pref+'$',name)or re.search((('[0-9]+,')*(multi+2))[0:-1]+'-'+'>'+str(multi)+'>'+'%{1,}'+numrad+pref+'$',name):
                                findings = re.findall('%{1,}'+numrad+pref+'$',name)
                                if findings:
                                    if self.debug:print1(self,'prefix 1,1-di % prop yl')
                                    positions = ['1']*(multi+2)
                                    recur_here = [True,findings[0].count('%')]
                                    name = re.sub((('[0-9]+,')*(multi+2))[0:-1]+'-'+'>'+str(multi)+'>'+'%{1,}'+numrad+pref+'$','',name)
                                else:
                                    if self.debug:print1(self,'prefix 1,1-di prop yl')
                                    positions = ['1']*(multi+2)
                                    name = re.sub((('[0-9]+,')*(multi+2))[0:-1]+'-'+'>'+str(multi)+'>'+numrad+pref+'$','',name)
                            #tri prop yl
                            if re.search('>'+str(multi)+'>'+numrad+pref+'$',name) or re.search('>'+str(multi)+'>'+'%{1,}'+numrad+pref+'$',name):
                                findings = re.search('%{1,}'+numrad+pref+'$',name)
                                if findings:
                                    if self.debug:print1(self,'prefix tri % prop yl')
                                    positions = ['1']*(multi+2)
                                    recur_here = [True,findings[0].count('%')]
                                    name =re.sub('>'+str(multi)+'>'+'%{1,}'+numrad+pref+'$','',name)
                                else:
                                    if self.debug:print1(self,'prefix tri prop yl')
                                    positions = ['1']*(multi+2)
                                    name = re.sub('>'+str(multi)+'>'+numrad+pref+'$','',name)
                    if not positions:
                        #1-prop yl
                        if re.search('[0-9]+-'+numrad+pref+'$',name) or re.search('[0-9]+-%*'+numrad+pref+'$',name):
                            findings = re.findall('%{1,}'+numrad+pref+'$',name)
                            if findings:
                                if self.debug:print1(self,'prefix 1-%prop yl')
                                recur_here = [True,findings[0].count('%')]
                                name = re.sub('[0-9]+-%{1,}'+numrad+pref+'$','',name)
                                positions = ['1']
                            else:
                                if self.debug:print1(self,'prefix 1-prop yl')
                                positions = ['1']
                                name = re.sub('[0-9]+-'+numrad+pref+'$','',name)
                        #propyl
                        elif re.search(numrad+pref+'$',name):
                            if '%' in name[-(len(numrad)+len(pref)+1):]:
                                if self.debug:print1(self,'prefix % propyl')
                                findings = re.search('%{1,}'+numrad+pref+'$',name)
                                positions = ['1']
                                recur_here = [True,findings[0].count('%')]
                                name = re.sub('%{1,}'+numrad+pref+'$','',name)
                            else:
                                if self.debug:print1(self,'prefix propyl')
                                positions = ['1']
                                name = re.sub(numrad+pref+'$','',name)
                        #1-yl
                        elif re.search('[0-9]+'+pref+'$',name):
                            if self.debug:print1(self,'prefix 1-yl')
                            positions = ['1']
                            name = re.sub('[0-9]+'+pref+'$','',name)
                        else:
                            pass
                    for i in positions:
                        todo,bonds = self.prefix_positions(i,pref,count,inside,recur_here,todo,depth,bonds,subs_count,name)
                        timer = 0
                    if positions:
                        positions = []
                        for bond in range(len(bonds)-1,-1,-1):
                            if len(bonds[bond])>2:
                                bonds.pop(bond)
                    recur_here = [False,0]
                name = re.sub('-$','',name)
                
        return name,todo,subs_count

    def recur(self,todo,depth,subs_count):
        if self.debug:print1(self,'in recur',subs_count)
        for i in todo[depth+1][subs_count]:
            if type(i) == type(''):
                self.add(i,todo[depth+1][subs_count][i])
            else:
                self.data['H']-=todo[depth+1][subs_count][i]*i
    
    def add(self,elm,count):
        self.data[elm]+=count
        self.data['H']-=2*count
        self.data['H']+=refdata[elm][0]*count
                
    
    def check_for_subsets(self,name,depth,todo,inside,subs_count):
        if self.debug:print1(self,'subsubsub')
        while re.search(r'\[.*\]',name):
            subs = re.search(r'\[.*\]',name)
            if not subs:
                break
            oind = name.index(subs[0])
            stack = 0
            ind = 0
            stack_loc = ['','']
            temp = subs[0]         
            while True:
                if temp[0] == '[':
                    if stack_loc[0] == '':
                        stack_loc[0] = ind
                    stack+=1
                elif temp[0] == ']':
                    stack -=1
                    if stack == 0:
                        stack_loc[1] = ind
                        break
                ind +=1
                temp=temp[1:]

            #do a recur
            tname = name[stack_loc[0]+oind+1:stack_loc[1]+oind]
            _,todo,sc = self.decode_prefix(tname,depth+1, todo ,True,subs_count)
            self.depth = depth
            name = name[0:stack_loc[0]+oind]+'%'*sc+name[stack_loc[1]+1+oind:]
        return name,todo

    def remove_bonds(self,name):
        total = 0
        bonds = []
        ynes = re.findall('(yne|yn|ene|en)',name)
        for yne in ynes:
            total = 0
            pos =  name.index(yne)
            if name[pos-1] == '>':
                multi = int(re.search('[0-9]+',name[pos-1-2:]).group())
                #1,1-dien
                findings = re.findall('-'+('[0-9]+,'*(multi+2))[0:-1]+'-'+'>'+str(multi)+'>'+yne,name)
                if findings:
                    if self.debug:print('rbonds 1,1-dien',pos,len(findings[0]),len(yne),name,findings)
                    total=(multi+2)*2
                    if yne in ['yne','yn']:
                        total+=(multi+2)*2
                    name = name.replace(findings[0],'',1)
                    bonds.append([pos-len(findings[0])+len(yne)-1,total])
                    continue
            #-1-yne
            if name[pos-1]=='-':
                findings = re.findall('-[0-9]+-'+yne,name)
                if findings:
                    
                    if self.debug:print('rbonds -1-dien',pos,len(findings[0]),len(yne),name,findings)
                    total=2
                    if yne in ['yne','yn']:
                        total+=2
                    name = name.replace(findings[0],'',1)
                    bonds.append([pos-len(findings[0])+len(yne)-1,total])
                    continue
            #yn
            if yne in name:
                if self.debug:print('rbonds en',pos,name)
                total=2
                if yne in ['yne','yn']:
                    total+=2
                name = name.replace(yne,'',1)
                bonds.append([pos-1,total])
                continue
            print('bond was unable to find place')
        return name,bonds
        

    def get_suffix(self,name,stack1):
        max_ = -1
        numm = -1
        for pref in prefixes:
            num = name.rfind(pref)
            if num>numm:
                numm = num
                max_ = len(pref)
        #sub out subs
        if '[' in name and ']' in name:
            a = name.index('[')
            b = name.rfind(']')
            if numm<b+1:
                numm = b+1
                max_ = 0
        if numm == -1:
            return name,''

        name1 = name[0:numm+max_]
        suffix = name[numm+max_:]
        return suffix,name1

    def prefix_positions(self,i,pref,count,inside,recur_here,todo,depth,bonds,subs_count,name):
        global true_todo
        if self.debug:print1(self,'prefix positions',i,pref,count)
        if inside == False:
            match pref:
                case 'yl':
                    self.add('C',count+1)
                case 'fluoro':
                    self.add('F',count+1)
                case 'chloro':
                    self.add('Cl',count+1)
                case 'bromo':
                    self.add('Br',count+1)
                case 'iodo':
                    self.add('I',count+1)
                case 'hydraxy':
                    self.add('O',count+1)
                case 'mercapto':
                    self.add('S',count+1)
                case 'imino':
                    self.add('N',count+1)
                    self.data['H']-=2
                case 'oxo':
                    self.add('O',count+1)
                    self.data['H']-=2
                case 'formkl':
                    self.add('C',count+1)
                    self.add('O',count+1)
                    self.data['H']-=2
                case 'carbaxy':
                    self.add('C',count+1)
                    self.add('O',count+1)
                    self.add('O',count+1)
                    self.data['H']-=2
                    
                case 'amido':
                    self.add('N',count+1)
                    self.add('O',count+1)
                    self.data['H']-=2
                    
                case 'amino':
                    self.add('N',count+1)
                case 'phosphino':
                    self.add('P',count+1)
                case 'arsino':
                    self.add('As',count+1)
                case 'oxy':
                    self.add('O',1)
                    self.add('C',count+1)
                case 'phunkl':
                    self.add('C',(count+1)*6)
                    self.data['H']-=(2*4)*(count+1)
                case 'axycarbankl':
                    self.add('C',1)
                    self.add('O',1)
                    self.add('O',1)
                    self.add('C',count+1)
                    self.data['H']-=2
                case 'oklaxy':
                    self.add('O',1)
                    self.add('C',count+1)
                    self.add('O',1)
                    self.data['H']-=2
                    
                case _:
                    for _ in range(20):
                        if self.debug:print1(self,'unknown prefix')
            if recur_here[0] == True:
                self.recur(todo,depth,recur_here[1])
            if bonds:
                if self.debug:print1(self,'prefix bonds',bonds,len(name))
                for bond in range(len(bonds)):
                    if len(name)< bonds[bond][0]:
                        self.data['H']-=bonds[bond][1]
                        if len(bonds[bond])==2:bonds[bond].append('True')
                    
               
                
        else:
            match pref:
                case 'yl':
                    todo[depth][subs_count]['C']+=count+1
                case 'fluoro':
                    todo[depth][subs_count]['F']+=count+1
                case 'chloro':
                    todo[depth][subs_count]['Cl']+=count+1
                case 'bromo':
                    todo[depth][subs_count]['Br']+=count+1
                case 'iodo':
                    todo[depth][subs_count]['I']+=count+1
                case 'hydraxy':
                    todo[depth][subs_count]['O']+=count+1
                case 'mercapto':
                    todo[depth][subs_count]['S']+=count+1
                case 'imino':
                    todo[depth][subs_count]['N']+=count+1
                    todo[depth][subs_count][1]+=2
                case 'oxo':
                    todo[depth][subs_count]['O']+=count+1
                    todo[depth][subs_count][1]+=2
                case 'formkl':
                    todo[depth][subs_count]['C']+=count+1
                    todo[depth][subs_count]['O']+=count+1
                    todo[depth][subs_count][1]+=2
                case 'carbaxy':
                    todo[depth][subs_count]['C']+=count+1
                    todo[depth][subs_count]['O']+=count+1
                    todo[depth][subs_count]['O']+=count+1
                    todo[depth][subs_count][1]+=2
                    
                case 'amido':
                    todo[depth][subs_count]['N']+=count+1
                    todo[depth][subs_count]['O']+=count+1
                    todo[depth][subs_count][1]+=2
                    
                case 'amino':
                    todo[depth][subs_count]['N']+=count+1
                case 'phosphino':
                    todo[depth][subs_count]['P']+=count+1
                case 'arsino':
                    todo[depth][subs_count]['As']+=count+1
                case 'oxy':
                    todo[depth][subs_count]['C']+=count+1
                    todo[depth][subs_count]['O']+=1
                case 'phunkl':
                    todo[depth][subs_count]['C']+=(count+1)*6
                    todo[depth][subs_count][1]+=(count+1)*8
                case 'axycarbankl':
                    todo[depth][subs_count]['C']+=1
                    todo[depth][subs_count]['O']+=1
                    todo[depth][subs_count]['O']+=1
                    todo[depth][subs_count]['C']+=count+1
                    todo[depth][subs_count][1]+=2
                case 'oklaxy':
                    todo[depth][subs_count]['O']+=1
                    todo[depth][subs_count]['O']+=1
                    todo[depth][subs_count]['C']+=count+1
                    todo[depth][subs_count][1]+=2
                case _:
                    for _ in range(20):
                        if self.debug:print1(self,'unknown prefix')
            if recur_here[0] == True:
                todo[depth][subs_count] = {k: todo[depth][subs_count].get(k, 0) + todo[depth+1][recur_here[1]].get(k, 0) for k in todo[depth][subs_count].keys() | todo[depth+1][recur_here[1]].keys()}

            if bonds:
                if self.debug:print1(self,'prefix inside bonds',bonds)
                for bond in range(len(bonds)):
                    if len(name)< bonds[bond][0]:
                        todo[depth][subs_count][1]+=bonds[bond][1]
                        if len(bonds[bond])==2:bonds[bond].append('True')
        return todo,bonds

    def reformat_name(self,name):
        repl = [
                ['meth','math'],
                ['undec','undac'],
                ['dodec','dodac'],
                ['tridec','trridac'],
                ['tetradec','teetradac'],
                ['puntadec','paantadac'],
                ['hexadec','haaxadac'],
                ['heptadec','haaptadac'],
                ['octadec','oaatadac'],
                ['nonadec','naanadac'],
                ['undeca','undaca'],
                ['dodeca','dodaca'],
                ['trideca','trridaca'],
                ['tetradeca','teetradaca'],
                ['puntadeca','paantadaca'],
                ['hexadeca','haaxadaca'],
                ['heptadeca','haaptadaca'],
                ['octadeca','oaatadaca'],
                ['nonadeca','naanadaca'],
                ['thiol','thikl'],
                ['carboxylic acid','carbaxklicacid'],
                ['carboxy','carbaxy'],
                ['hydroxy','hydraxy'],
                ['phenyl','phunkl'],
                ['oxycarbonyl','axycarbankl'],
                ['oyloxy','oklaxy'],
                ['anoklaxy','oklaxy'],
                ['formyl','formkl'],
                [' acid','acid'],
                ['non','nin'],
                ['nine','nome'],
                ['nomen','ninen'],
                ['one','ome'],
                ['ether','ither'],
                ['nona','nina'],
                
                ]

        self.rr = {
            '<0<':0,
            '<1<':1,
            '<2<':2,
            '<3<':3,
            '<4<':4,
            '<5<':5,
            '<6<':6,
            '<7<':7,
            '<8<':8,
            '<9<':9,
            '<10<':10,
            '<11<':11,
            '<12<':12,
            '<13<':13,
            '<14<':14,
            '<15<':15,
            '<16<':16,
            '<17<':17,
            '<18<':18,
            }
        self.mr = {
            '>0>':0,
            '>1>':1,
            '>2>':2,
            '>3>':3,
            '>4>':4,
            '>5>':5,
            '>6>':6,
            '>7>':7,
            '>8>':8,
            '>9>':9,
            '>10>':10,
            '>11>':11,
            '>12>':12,
            '>13>':13,
            '>14>':14,
            '>15>':15,
            '>16>':16,
            '>17>':17,
            }

        if re.search('benzene$',name):
                    name = re.sub('benzene','cyclohex-2,4,6-triene',name)
                    if self.debug:print1(self,name)
        for yne in ynes:
            if re.search(yne+'$',name):
                name+='ane'
        name = re.sub('pent','punt',name)
        tname = name
        
        while '[' in tname or ']' in tname:
            subs = re.search(r'\[.*\]',tname)
            if subs:
                oind = tname.index(subs[0]) 
                #stack
                stack = 0
                ind = 0
                stack_loc = ['','']
                temp = subs[0]
                while True:
                    if temp[0] == '[':
                        if stack_loc[0] == '':
                            stack_loc[0] = ind
                        stack+=1
                    elif temp[0] == ']':
                        stack -=1
                        if stack == 0:
                            stack_loc[1] = ind
                            break
                    ind +=1
                    temp=temp[1:]   
                tname = tname[0:stack_loc[0]+oind]+tname[stack_loc[1]+1+oind:]
                if(self.debug):print1(tname)
            else:break
        
        
        omult = [         "di",     "tri",     "tetra",     "punta",     "hexa",     "hepta",     "octa",     "nona",     "deca", 
              "undeca", "dodeca", "trideca", "tetradeca", "puntadeca", "hexadeca", "heptadeca", "octadeca", "nonadeca"]

        stack1 = []
        counter1 = 0
        timer1 = 0
        while True:
            timer1 +=1
            for mult_ind in range(len(omult)-1,-1,-1):
                key = omult[mult_ind]
                if not re.search(('[0-9]+,'*(mult_ind+3))[0:-1]+'-'+key,name):
                    findings = re.search(('[0-9]+,'*(mult_ind+2))[0:-1]+'-'+key,name)
                    if findings:
                        timer1 = 0
                        stack1.append([counter1,findings[0]])
                        name = name.replace(findings[0],'%'+str(counter1)+'%',1)
                        counter1+=1
            if timer1 >1:break
            
        if self.debug:print('stack1', stack1)
        

        stack = []
        counter = 0
        timer = 0
        if self.debug:print('after repl stack',name)
        while True:
            timer +=1
            for pref in ['fluoro$','chloro$','bromo$','iodo$','mercapto$',
                             'imino$','oxo$','amido$',
                             'amino$','phosphino$','arsino$',
                             ][::-1]:
                if pref.replace('$','') in name:
                    timer = 0
                    stack.append([counter,pref.replace('$','')])
                    name = name.replace(pref.replace('$',''),'@'+str(counter)+'@',1)
                    counter+=1
        
            if timer > 3:break
        if(self.debug):print1(name)
        for i in repl:name = name.replace(i[0],i[1])
        for i in stack:
            name = name.replace('@'+str(i[0])+'@',i[1])
        
        
        if self.debug:print1(self,'after stack',name)
        

                
        #replace all with new mr,rr
        for rad in range(len(radicals)-1,-1,-1):
            name = name.replace(radicals[rad],list(self.rr.keys())[rad])
        for multi in range(len(multipliers)-1,-1,-1):
            name = name.replace(multipliers[multi],list(self.mr.keys())[multi])

        for i in stack1:
            name = name.replace('%'+str(i[0])+'%',i[1])
        for i in repl:name = name.replace(i[0],i[1])
        
        #replace all with new mr,rr again
        for multi in range(len(multipliers)-1,-1,-1):
            name = name.replace(multipliers[multi],list(self.mr.keys())[multi])
        if 'oate' in name[-4:] and ' ' in name:
            toggle = False
            if self.debug:print('esters',name)
            if '>' in name[-4-1:]:
                multi = int(re.findall('[0-9]+',name[-4-1-2:])[0])
                #-1,2-di oate
                findings = re.search('-'+('[0-9]+,'*(multi+2))[0:-1]+'-'+'>'+str(multi)+'>'+'oate$',name)
                if findings:
                    toggle = True
                    esterpos = re.findall('[0-9]+',findings[0])[:-1]
                    if self.debug:print('esterpos',esterpos)
                    split = name.split(' ')
                    split[0] = ','.join(esterpos)+'-'+'>'+str(multi)+'>'+split[0]
                    split[1] = '-'+split[1]
                    name = ''.join(split)
            if not toggle:
                #did not find above
                if self.debug:print('ester variation2')
                esterpos = ['1']
                split = name.split(' ')
                split[0] = ','.join(esterpos)+'-'+split[0]
                split[1] = '-'+split[1]
                name = ''.join(split)
            if self.debug:print('esters_end',name)   

        if self.debug:print1(self,'translated:',name)
        if self.debug:print('untranslated:',name)

        return name,stack1

    def print1er(self):
        res = {}
        for i in self.data:
            if self.data[i]!=0:
                res[i] = self.data[i]
        if self.debug:print1(self,res)
        
def print1(*args):
    if isinstance(args[0],ParseHer1):
        #includes the 'self' attribute
        self = args[0]
        args = args[1:]
        tabs = (self.depth)*' '
    else: tabs = ''
        
    rr = {
        '<0<':0,
        '<1<':1,
        '<2<':2,
        '<3<':3,
        '<4<':4,
        '<5<':5,
        '<6<':6,
        '<7<':7,
        '<8<':8,
        '<9<':9,
        '<10<':10,
        '<11<':11,
        '<12<':12,
        '<13<':13,
        '<14<':14,
        '<15<':15,
        '<16<':16,
        '<17<':17,
        '<18<':18,
        }
    mr = {
        '>0>':0,
        '>1>':1,
        '>2>':2,
        '>3>':3,
        '>4>':4,
        '>5>':5,
        '>6>':6,
        '>7>':7,
        '>8>':8,
        '>9>':9,
        '>10>':10,
        '>11>':11,
        '>12>':12,
        '>13>':13,
        '>14>':14,
        '>15>':15,
        '>16>':16,
        '>17>':17,
        }
    arr = []
    for i in args:
        for r in rr:
            try:
                i=i.replace(r,radicals[rr[r]])
            except:pass
        for r in mr:
            try:
                i=i.replace(r,multipliers[mr[r]])
            except:pass
        arr.append(i)
    print(tabs,*(arr))
