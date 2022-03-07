class Inspector:
    def __init__(self):
        self.allowC = []
        self.disallowC = []
        self.passportRequired = True
        self.wanted = ''
        self.foreignpermit = False
        self.idcard = False
        self.workpass = False
        self.vacc = []
    
    def inspect(self,obj):
        self.papers = []
        self.id = []
        self.name = []
        self.nation = []
        self.dob = []
        self.access = []
        self.height = []
        self.weight = []
        self.vaccines = []
        self.purpose = []
        self.exp = []

        self.failures = []

        if 'passport' in obj:
            self.papers.append('passport')
            self.id.append(obj['passport'][obj['passport'].index('ID#:')+5:obj['passport'].index('ID#:')+16])
            self.name.append(obj['passport'][obj['passport'].index('NAME')+6:obj['passport'].index('\n',obj['passport'].index('NAME'))])
            self.nation.append(obj['passport'][obj['passport'].index('NATION')+8:obj['passport'].index('\n',obj['passport'].index('NATION'))])
            self.dob.append(obj['passport'][obj['passport'].index('DOB')+5:obj['passport'].index('\n',obj['passport'].index('DOB'))])
            self.exp.append(obj['passport'][obj['passport'].index('EXP')+5:obj['passport'].index('EXP')+16])
        if 'access_permit' in obj:
            self.papers.append('access permit')
            self.id.append(obj['access_permit'][obj['access_permit'].index('ID#:')+5:obj['access_permit'].index('ID#:')+16])
            self.name.append(obj['access_permit'][obj['access_permit'].index('NAME')+6:obj['access_permit'].index('\n',obj['access_permit'].index('NAME'))])
            self.purpose.append(obj['access_permit'][obj['access_permit'].index('PURPOSE')+9:obj['access_permit'].index('\n',obj['access_permit'].index('PURPOSE'))])
            self.nation.append(obj['access_permit'][obj['access_permit'].index('NATION')+8:obj['access_permit'].index('\n',obj['access_permit'].index('NATION'))])
            self.height.append(obj['access_permit'][obj['access_permit'].index('HEIGHT')+8:obj['access_permit'].index('\n',obj['access_permit'].index('HEIGHT'))])
            self.weight.append(obj['access_permit'][obj['access_permit'].index('WEIGHT')+8:obj['access_permit'].index('\n',obj['access_permit'].index('WEIGHT'))])
            self.exp.append(obj['access_permit'][obj['access_permit'].index('EXP')+5:obj['access_permit'].index('EXP')+16])
        if 'grant_of_asylum' in obj:
            self.papers.append('grant of asylum')
            self.id.append(obj['grant_of_asylum'][obj['grant_of_asylum'].index('ID#:')+5:obj['grant_of_asylum'].index('ID#:')+16])
            self.name.append(obj['grant_of_asylum'][obj['grant_of_asylum'].index('NAME')+6:obj['grant_of_asylum'].index('\n',obj['grant_of_asylum'].index('NAME'))])
            self.nation.append(obj['grant_of_asylum'][obj['grant_of_asylum'].index('NATION')+8:obj['grant_of_asylum'].index('\n',obj['grant_of_asylum'].index('NATION'))])
            self.height.append(obj['grant_of_asylum'][obj['grant_of_asylum'].index('HEIGHT')+8:obj['grant_of_asylum'].index('\n',obj['grant_of_asylum'].index('HEIGHT'))])
            self.weight.append(obj['grant_of_asylum'][obj['grant_of_asylum'].index('WEIGHT')+8:obj['grant_of_asylum'].index('\n',obj['grant_of_asylum'].index('WEIGHT'))])
            self.exp.append(obj['grant_of_asylum'][obj['grant_of_asylum'].index('EXP')+5:obj['grant_of_asylum'].index('EXP')+16])
        if 'work_pass' in obj:
            self.papers.append('work_pass')
            self.name.append(obj['work_pass'][obj['work_pass'].index('NAME')+6:obj['work_pass'].index('\n',obj['work_pass'].index('NAME'))])
            self.exp.append(obj['work_pass'][obj['work_pass'].index('EXP')+5:obj['work_pass'].index('EXP')+16])
        if 'diplomatic_authorization' in obj:
            self.id.append(obj['diplomatic_authorization'][obj['diplomatic_authorization'].index('ID#:')+5:obj['diplomatic_authorization'].index('ID#:')+16])
            self.name.append(obj['diplomatic_authorization'][obj['diplomatic_authorization'].index('NAME')+6:obj['diplomatic_authorization'].index('\n',obj['diplomatic_authorization'].index('NAME'))])
            self.nation.append(obj['diplomatic_authorization'][obj['diplomatic_authorization'].index('NATION')+8:obj['diplomatic_authorization'].index('\n',obj['diplomatic_authorization'].index('NATION'))])
            for eachC in obj['diplomatic_authorization'][obj['diplomatic_authorization'].index('ACCESS')+8:].split(', '):
                self.access.append(eachC)
        if 'certificate_of_vaccination' in obj:
            self.id.append(obj['certificate_of_vaccination'][obj['certificate_of_vaccination'].index('ID#:')+5:obj['certificate_of_vaccination'].index('ID#:')+16])
            self.name.append(obj['certificate_of_vaccination'][obj['certificate_of_vaccination'].index('NAME')+6:obj['certificate_of_vaccination'].index('\n',obj['certificate_of_vaccination'].index('NAME'))])
            for eachC in obj['certificate_of_vaccination'][obj['certificate_of_vaccination'].index('VACCINES')+10:].split(', '):
                self.vaccines.append(eachC)
        if 'ID_card' in obj:
            self.name.append(obj['ID_card'][obj['ID_card'].index('NAME')+6:obj['ID_card'].index('\n',obj['ID_card'].index('NAME'))])
            self.dob.append(obj['ID_card'][obj['ID_card'].index('DOB')+5:obj['ID_card'].index('\n',obj['ID_card'].index('DOB'))])
            self.height.append(obj['ID_card'][obj['ID_card'].index('HEIGHT')+8:obj['ID_card'].index('\n',obj['ID_card'].index('HEIGHT'))])
            self.weight.append(obj['ID_card'][obj['ID_card'].index('WEIGHT')+8:])

        if len(self.name) > 0:
            if self.name[0] == self.wanted:
                self.failures.append('criminal')
                
        if not all(element==self.id[0] for element in self.id):
            self.failures.append('id m')
        if not all(elemen==self.name[0] for elemen in self.name):
            self.failures.append('name m')
        if not all(eleme==self.nation[0] for eleme in self.nation):
            self.failures.append('nat m')
        if not all(elem==self.dob[0] for elem in self.dob):
            self.failures.append('dob m')

        if self.passportRequired:
            if 'passport' not in obj:
                self.failures.append('no pass')
        if 'diplomatic_authorization' in obj:
            if 'Arstotzka' not in self.access:
                self.failures.append('bad dipo')                
        if self.foreignpermit:
            if len(self.nation) > 0:
                if self.nation[0] != 'Arstotzka':
                    if 'access_permit' not in obj:
                        if 'grant_of_asylum' not in obj and 'diplomatic_authorization' not in obj:
                            self.failures.append('no perm')
        if self.idcard:
            if len(self.nation) > 0:
                if self.nation[0] == 'Arstotzka':
                    if 'ID_card' not in obj:
                        self.failures.append('no id')
        if self.workpass:
            if len(self.purpose) > 0:
                if self.purpose[0] == 'WORK':
                    if 'work_pass' not in obj:
                        self.failures.append('no work')                
        for dates in range(len(self.exp)):
            if int(self.exp[dates][:4]) < 1982:
                self.failures.append('Entry denied: '+self.papers[dates]+' expired.')
            else:
                if int(self.exp[dates][:4]) == 1982 and int(self.exp[dates][5:-3]) < 11:
                    self.failures.append('Entry denied: '+self.papers[dates]+' expired.')
                else:
                    if int(self.exp[dates][:4]) == 1982 and int(self.exp[dates][5:-3]) == 11 and int(self.exp[dates][-2:]) < 22: #possibly <=
                        self.failures.append('Entry denied: '+self.papers[dates]+' expired.')

        for disease in range(len(self.vacc)):
            if len(self.nation) > 0:
                if self.nation[0] in self.vacc[disease]:
                    if self.vacc[disease-1] not in self.vaccines:
                        self.failures.append('no vac')
                        break

        if len(self.nation) > 0:
            if self.nation[0] in self.disallowC or self.nation[0] not in self.allowC:
                self.failures.append('bann')
            if self.nation[0] == 'Arstotzka' and len(self.failures) < 1:
                return 'Glory to Arstotzka.'
            if self.nation[0] != 'Arstotzka' and len(self.failures) < 1:
                return 'Cause no trouble.'
        
        fail = {'criminal':'Detainment: Entrant is a wanted criminal.',
                'id m':'Detainment: ID number mismatch.',
                'name m':'Detainment: name mismatch.',
                'nat m':'Detainment: nationality mismatch.',
                'dob m':'Detainment: date of birth mismatch.',
                'no pass':'Entry denied: missing required passport.',
                'no perm':'Entry denied: missing required access permit.',
                'no id':'Entry denied: missing required ID card.',
                'no work':'Entry denied: missing required work pass.',
                'bad dipo':'Entry denied: invalid diplomatic authorization.',
                'bann':'Entry denied: citizen of banned nation.',
                'no vac':'Entry denied: missing required vaccination.'}
        if self.failures[0] in fail:
            return fail[self.failures[0]]
        return self.failures[0]

    def receive_bulletin(self,bull):
        arr = bull.split('\n')
        self.wanted = ''
        for i in range(len(arr)):
            if 'Entrants require passport' in arr[i]:
                self.passportRequired = True
            if 'Allow citizens of ' in arr[i]:
                for j in arr[i][18:].split(', '):
                    self.allowC.append(j)
                    try:
                        self.disallowC.remove(j)
                    except:
                        continue
            if 'Wanted by the State: ' in arr[i]:
                self.wanted = arr[i][arr[i].index(' ',arr[i].index('State: ')+8)+1:]+', '+arr[i][arr[i].index('State: ')+7:arr[i].index(' ',arr[i].index('State')+7)]
            if 'Foreigners require access permit' in arr[i]:
                self.foreignpermit = True
            if 'Citizens of Arstotzka require ID card' in arr[i]:
                self.idcard = True
            if 'Deny citizens of ' in arr[i]:
                for j in arr[i][17:].split(', '):
                    self.disallowC.append(j)
                    try:
                        self.allowC.remove(j)
                    except:
                        continue
            if 'Workers require work pass' in arr[i]:
                self.workpass = True
            Entrants = ['Arstotzka', 'Antegria', 'Impor', 'Kolechia','Obristan', 'Republia','United Federation']
            Foreigners = ['Antegria', 'Impor', 'Kolechia','Obristan', 'Republia','United Federation']
            done = 0
            if 'Foreigners require ' in arr[i] and 'vaccination' in arr[i]:
                for j in range(len(self.vacc)):
                    if arr[i][19:-12] in self.vacc[j]:
                        self.vacc[j+1] = Foreigners
                        done = 1
                if done == 0:
                    self.vacc.append(arr[i][19:-12])
                    self.vacc.append(Foreigners)
            done = 0
            if 'Entrants require ' in arr[i] and 'vaccination' in arr[i]:
                for j in range(len(self.vacc)):
                    if arr[i][17:-12] in self.vacc[j]:
                        self.vacc[j+1] = Entrants
                        done = 1
                if done == 0:
                    self.vacc.append(arr[i][17:-12])
                    self.vacc.append(Entrants)
            if 'Entrants no longer require ' in arr[i] and 'vaccination' in arr[i]:
                for j in range(len(self.vacc)):
                    if arr[i][27:-12] in self.vacc[j]:
                        self.vacc[j+1] = []
            if 'Foreigners no longer require ' in arr[i] and 'vaccination' in arr[i]:
                for j in range(len(self.vacc)):
                    if arr[i][29:-12] in self.vacc[j]:
                        self.vacc[j+1] = []
            done = 0
            if 'Citizens of' in arr[i] and 'vaccination' in arr[i] and 'no' not in arr[i]:
                for j in range(len(self.vacc)):
                    if arr[i][arr[i].index('require')+8:-12] in self.vacc[j]:
                        self.vacc[j+1] = []
                        done = 1
                if done == 0:
                    self.vacc.append(arr[i][arr[i].index('require')+8:-12])
                    self.vacc.append(arr[i][12:arr[i].index('require')-1].split(', '))
                    
            if 'Citizens of' in arr[i] and 'vaccination' in arr[i] and 'no' in arr[i]:
                for j in range(len(self.vacc)):
                    if arr[i][arr[i].index('no longer require')+18:-12] in self.vacc[j]:
                        self.vacc[j+1] = []
