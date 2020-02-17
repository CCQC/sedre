#!/usr/bin/env python
# coding: utf-8

# In[17]:


import sedre
#import oss
#import dawgspec as ds


# In[18]:


pglib = {'C2v':{'A1':[1,1,1,1],'A2':[1,1,-1,-1],'B1':[1,-1,1,-1], 'B2':[1,-1,-1,1]}, 'Cs':{'A\'':[1,1],'A\"':[1,-1]},'C3v':{'A1':[1,1,1],'A2':[1,1,-1],'E':[2,-1,0]},'Ci':{'Ag':[1,1],'Au':[1,-1]}, 'D2h':{'Ag':[1,1,1,1,1,1,1,1],'B1g':[1,1,-1,-1,1,1,-1,-1],'B2g':[1,-1,1,-1,1,-1,1,-1],'B3g':[1,-1,-1,1,1,-1,-1,1],'Au':[1,1,1,1,-1,-1,-1,-1],'B1u':[1,1,-1,-1,-1,-1,1,1],'B2u':[1,-1,1,-1,-1,1,-1,1],'B3u':[1,-1,-1,1,-1,1,1,-1]}}


# In[19]:


def dotinto(pg, irrep_1, irrep_2):
    #dots two irreps from a given point group and returns the corresponding irrep
    dotprod = []
    c=0
    for i in range(len(pglib[pg][irrep_1])):
        dotprod.append(pglib[pg][irrep_1][i]*pglib[pg][irrep_2][i])
    for key in pglib[pg]:
        if pglib[pg][key]==dotprod:
            c+=1
            return key
    if c == 0:
        return '--'
        
    


# In[ ]:


def clean_orbital_list(section, file = 'output.dat'):
    #takes a section found by sedre and returns a list of orbital symmetries
    if sedre.Parser(program = 'qchem', filename = file).data['properties']['TDDFT']['pg']['vals'][0][0] =='C1':
        return None
    else:
        lst1 = section.split('\n')
        lst2 = []
        for item in lst1:
            for i in range(len(item.split())):
                lst2.append(item.split()[i])
        lst3 = []
        lst4 = []
        lst5 = []
        for item in lst2:
            if item.strip(' -') == '':
                continue
            else:
                lst3.append(item)
        for item in lst3:
            if item =='':
                continue
            else:
                lst5.append(item)
        for item in lst5:
            for i in range(len(item)):
                if item[0] in ['0','1','2','3','4','5','6','7', '8','9','V','-']:
                    continue
                else:
                    lst4.append(item)
                    break
        return lst4


# In[21]:


def v_orbital_symmetries(file = 'output.dat'):
    #gives virtual orbital symmetries from a specified output file
    with open(file, 'r') as f: output = f.read()
    f=open(file)
    lines=f.readlines()
    section =lines[sedre.Parser(program = 'qchem', filename = file).data['sections']['TDDFT']['vir_orbitals']['hits'][0][0]:sedre.Parser(program = 'qchem', filename = file).data['sections']['TDDFT']['vir_orbitals']['hits'][0][1]]
    cleaner_section = ''.join(section)
    return clean_orbital_list(cleaner_section,file)
                              
def o_orbital_symmetries(file = 'output.dat'):
    #gives occupied orbital symmetries from a specified output file
    with open(file, 'r') as f: output = f.read()
    f=open(file)
    lines=f.readlines()
    section =lines[sedre.Parser(program = 'qchem', filename = file).data['sections']['TDDFT']['occ_orbitals']['hits'][0][0]:sedre.Parser(program = 'qchem', filename = file).data['sections']['TDDFT']['occ_orbitals']['hits'][0][1]]
    cleaner_section = ''.join(section)
    return clean_orbital_list(cleaner_section,file)
                              
def orbital_symmetries(file = 'output.dat'):
    #gives all orbital symmetries from a specified output file
    list_all_sym = o_orbital_symmetries(file)+v_orbital_symmetries(file)
    return list_all_sym


# In[22]:

def return_trans_sym(file = 'output.dat'):
    # returns a list of transition symmetries from a qchem TDDFT output.dat file in order of increasing excitation energies
    
    # if the molecule is C1, all transitions are of A symmetry... 
    # this will return a list of As of the appropriate length 
    # if the point group is detected to be C1
    if sedre.Parser(program = 'qchem', filename = file).data['properties']['TDDFT']['pg']['vals'][0][0] =='C1':
        return ['A']*len(sedre.Parser(program = 'qchem', filename = file).data['energy']['TDDFT']['exc']['vals'][0])
    else:
        lst_1 = []
        lst_2 = []
        lst_3 = []
        lst4 = []
        property_list = []

        # read the file and temporarily save the lines
        with open(file, 'r') as f: output = f.read()
        f=open(file)
        lines=f.readlines()

        # iterate through each line in lines
        # remove extraneous spaces
        # append cleaned line to lst_1
        for line in list(lines):
            new_line = line.strip(' ')
            lst_1.append(new_line)
            
        # iterate through each cleaned line in lst_1
        # append the line 5 lines after any line that contains the word 'Excited' to lst_2
        # (this is the line that contains the D() --> V() information)
        for i in range(len(lst_1)):
            if 'Excited' in lst_1[i].split(' '):
                lst_2.append(lst_1[i+5])

        # finds the point group of the molecule with sedre in the output.dat file
        # uses sedre functions to get the symmetries of the occupied, virtual, and all orbitals
        pg = sedre.Parser(program = 'qchem', filename = file).data['properties']['TDDFT']['pg']['vals'][0][0]
        occ_orb_sym = sedre.o_orbital_symmetries(file)
        vir_orb_sym = sedre.v_orbital_symmetries(file)
        all_orb_sym = sedre.orbital_symmetries(file)


        # grabs the orbital numbers from D(m) --> V(n) line
        # remove extraneous spaces
        # append orbital numbers m, n to lst_3
        for item in lst_2:
            orbitals = [int((item[2]+item[3]+item[4]).strip(' ')),int((item[13]+item[14]+item[15]).strip(' '))]
            lst_3.append(orbitals)

        # re-indexes the orbital numbers so that each orbital has a unique number
        # virtual orbitals start at ('number of occupied orbitals' + 1)
        for i in range(len(lst_3)):
            num_occ_orb = len(occ_orb_sym)
            new_item = [int(lst_3[i][0]),int(lst_3[i][1])+num_occ_orb]
            lst4.append(new_item)

        # appends the symmetries of the origin orbital, destination orbital, 
        # and transition (product of the previous two symmetries)
        for i in range(len(lst4)):
            lst4[i].append(all_orb_sym[int(lst4[i][0])-1])
            lst4[i].append(all_orb_sym[int(lst4[i][1])-1])
            lst4[i].append(sedre.dotinto(pg,lst4[i][2],lst4[i][3]))
            property_list.append(lst4[i][4])
        return property_list



