"""Output file parser for quantum chemistry.
Intended to be easy, logical to use. Should be quickly incorporable
into workflow by high level functions and objects.
Requires only the Python standard library, sed, and sedre's submodules

Should be agnositic to Python 3.X version,
but was written in Spring 2019 so tested exclusively on Python 3.7.3

nstructions for adding a lookup file
Make a file in sedre/lookups/ with title <program_name>.py
look at an existing file for guidance, make sure to import common
write the lookup file. Section delims are passed directly to sed, so they
need to be formatted s.t. they work with sed (slightly unintuitive)
Energy, properties are regular expressions that only search within the
text sections produced by slicing the file into chunks at the section delimiters.
To sedre/lookups/_init_.py add a line:
from .<program_name> import lookup
In sedre.py add a line with the other elifs:
elif program is '<program_name>':
    self.<program_name>()

Then add a function with the other program names:
def <program_name>(self):
    self.lookup = copy.deepcopy(lookups.<program_name>.lookup)

###############################
#Data management and import
###############################
#load() converts the output file into two forms, str and list.
#str is easy to search with a global (not restricted to a block) regex
#list makes it easy to take the sections of the computations and search
#..only within a certain type. e.g. get HF dipole by just finding 'dipole'
#..w/in the HF section
###############################
"""

#Modules imported from Python Standard Library
#
import sys
import os
import subprocess as sp
import re
import json
import copy
from time import time

#Imports from
#Submodules
from . import lookups 
from . import common

class Parser:
    def __init__(self,filename='output.dat',program=None,indict=None):
        assert type(filename) == str
        assert (type(program) == str) or (program == None)
        assert (type(indict) == dict) or (indict == None)
        self.file = filename
        self.program = program
        self.content = {}        
        self.lookup = {}
        self.data = {}
        
        if program is None:
            return
        
        elif program is 'molpro':
            self.molpro() #started
            
        elif program is 'orca':
            self.orca()
            
        elif program is 'psi4':
            self.psi4()
            
        elif program is 'qchem':
            self.qchem()
            
        elif program is 'cfour':
            self.cfour() #started, confusing
        
        elif program is 'mrcc':
            self.mrcc()
            
        elif program is 'gaussian':
            try:
                pass
            except:
                raise ValueError('Gaussian is NOT supported.')

        if indict is not None:
            self.data = indict
                
        elif self.load():
            self.get_line_numbers(self.lookup,self.data)
            #self.lines_to_blocks()
            self.lines_to_blocks2(self.data['sections'])
            #self.scrape()
            self.scrape2(self.lookup['energy'],self.data['sections'],self.data['energy'])
            self.scrape2(self.lookup['properties'],self.data['sections'],self.data['properties'])
        else:
            print('Problem loading file.\nNo data loaded.')
    def molpro(self):
        """Grabs core MOLPRO regexes.
        
        Written using version 2010.1.67 output files."""
        self.lookup = copy.deepcopy(lookups.molpro.lookup) #need deepcopy s.t. two parser() instances for the same program
                                                              #can be open simultaneously
       
    def cfour(self):
        "Grabs core CFOUR regexes"
        self.lookup = copy.deepcopy(lookups.cfour.lookup)
        
    def orca(self):
        """Grabs core ORCA regexes.
        
        Written using version 4.X output files."""
        self.lookup = copy.deepcopy(lookups.orca.lookup)
                                             
    def psi4(self):
        """Grabs core Psi4 regexes.
        
        Written using version 1.2/1.3 output files."""
        self.lookup = copy.deepcopy(lookups.psi4.lookup)
    
    def mrcc(self):
        "Grabs core MRCC regexes"
        self.lookup = copy.deepcopy(lookups.mrcc.lookup)
    
    def qchem(self):
        """Grabs core QChem regexes.

        Written using version 5.0 output files."""
        self.lookup = copy.deepcopy(lookups.qchem.lookup)
    
    def look_for(self,rstr,lines=None):
        """looks for regular expression in self.content.

        Inputs
            rstr : regular expression to search for.
            lines=None : line numbers to search between.
        """
        
        if type(rstr) is not str:
            return None

        if lines is not None:
            startline,endline = lines
            temp = ''.join(self.content['list'][startline:endline])
            #print(temp)
        else:
            temp = self.content['str']
        result = re.findall(rstr,temp)
        return result
    
    def line_num(self,rstr,lines=None):
        if lines is not None:
            startline,endline = lines
            temp = ''.join(self.content['list'][startline:endline])
        else:
            temp = self.content['str']
        #result = common.line_num()

    def load(self):
        """
        Called first when opening a Parser object.
        Loads file contents into self.content.

        self.content['str'] is contents in raw string form.
        self.contents['list'] is contents in list of lines.
        """
        if os.path.isfile(self.file):
            with open(self.file,'r') as f: self.content['str'] = f.read()
            with open(self.file,'r') as f: self.content['list'] = f.readlines()
            return True
        else:
            return False

    def get_line_numbers(self,indict,outdict,clean=False):
        """
        Uses lookup information (self.lookup) and contents (self.content)
        to find line numbers for all regular expressions.

        For sections, these are 'start' and 'end' lines to be processed
        into sections of the file.

        """
        if type(indict) != dict:
            return
        else:
            for key in indict:
                if key in outdict:
                    return
                if type(indict[key]) == dict:
                    outdict[key] = {}
                    if key == 'energy':
                        ctemp = True
                    else:
                        ctemp = clean
                    self.get_line_numbers(indict[key],outdict[key],clean=ctemp) #recursive
                elif type(indict[key]) == str:
                    outdict[key] = {}
                    if clean:
                        continue
                    else:
                        outdict[key]['ln'] = common.line_num(indict[key],self.file) #ln = line numbers
                else:
                    return
    
    def lines_to_blocks(self):
        """
        ###############################
        #lines_to_blocks is called after load() and get_line_numbers()
        #uses sed commands to take line information
        #..and turn it into blocks.
        ###############################
        """
        for key in self.lookup['sections']:
            if self.data['sections'][key]['start']['ln'] is None:
                self.data['sections'][key]['hits'] = None
                continue
            
            sections = []
            for i in self.data['sections'][key]['start']['ln']:
                if (len(sections) > 0) and (i <= sections[-1][1]):
                    continue
                for j in self.data['sections'][key]['end']['ln']:
                    #find closest end after each start
                    if i < j:
                        sections.append((i,j))
                        break
            self.data['sections'][key]['hits'] = sections

    def lines_to_blocks2(self,indict):#,outdict):
        """
        (experimental)
        recursive version of sedre.Parser.lines_to_blocks() for upcoming
        subsection feature implementation.
        """
        if type(indict) != dict:
            return

        if ('start' in indict.keys()) and ('end' in indict.keys()):
            #then this is a section
            hits=[]
            if (indict['start']['ln'] is not None) and (indict['end']['ln'] is not None):
                for i in indict['start']['ln']:
                    #if (len(hits) > 0) and (i <= sections[-1][1]):
                    #    continue
                    for j in indict['end']['ln']:
                        #find closest end after each start
                        if i < j:
                                hits.append((i,j))
                                break #break so we dont make more than one hit from each start match
            indict['hits'] = hits

        for key in indict:
            #print(key)
            if (indict[key] not in ('start','end')) and (type(indict[key]) == dict):
                #then this is a subsection dict
                #what to do?
                self.lines_to_blocks2(indict[key])
                pass
          
    def scrape2(self,lookup,section,data,supersection=False):
       # if (not supersection) and ('hits' not in section.keys()): 
       #     """
       #     #then we're not a baby section, so we should have our own
       #     #list of hits!
       #     #shouldn't happen
       #     """
       #     return

       # if 'hits' in section.keys():
       #     #then we are looking at a section of some kind
#       print(section)
       for attribute in lookup:
           if attribute not in data:
               data[attribute] = {}
            
           if type(lookup[attribute]) == dict:
               #then its either a subsection or a point of distinction
               if attribute in section.keys() and 'hits' in section[attribute].keys(): 
                   #then its a subsection, and we don't need a supersection
                   self.scrape2(lookup[attribute],section[attribute],data[attribute]) #recursive
               else:
                   #then its a point of distinction
                   self.scrape2(lookup[attribute],section,data[attribute]) #recursive with implicit supersection

           elif type(lookup[attribute] == str) and ('hits' in section.keys()) and (len(section['hits']) > 0):
               data[attribute]['vals'] = [] #make a list to hold numeric values
               #then we should use the regex
               for hit in section['hits']:
                   data[attribute]['vals'].append(self.look_for(lookup[attribute],lines=list(hit))) 
           else:
               pass
            
    def scrape(self,subset=['energy','properties']):
        """
        ###############################
        #scrape() is called after lines_to_blocks()
        #scrape() searches for energy and property regexes
        #..within the appropriate blocks.
        ###############################
        """
        for sub in subset:
            for key in self.data['sections']:
                hits = self.data['sections'][key]['hits']
                if hits is not None and (key in self.data[sub].keys()):
                    for attribute in self.data[sub][key]:
                        if self.data[sub][key][attribute] is None:
                            self.data[sub][key][attribute] = {}
                        self.data[sub][key][attribute]['vals'] = []
                        rstr = self.lookup[sub][key][attribute]
                        if type(rstr) != str:
                            continue #TODO: need a way to read in subsections e.g. molpro MRCI corrections
                        for hit in hits:
                            #print(type(hit))
                            #print(type(sub))
                            #print(type(key))
                            #print(type(attribute))
                            #print(type(rstr))
                            #print(rstr)
                            self.data[sub][key][attribute]['vals'].append(self.look_for(rstr,lines=list(hit)))
        
    def pickup(self):
        "returns JSON dump"
        return json.dumps(self.data)

    def write(self,fname=None):
        """writes to a file
        .sdf -> sedre dump file
        
        fname=None : optional filename. If not given then
        quickwrite_<datetime>.sdf"""
        assert not os.path.isfile(fname)
        if fname:
            t = fname
        else:
            t = 'quickwrite_'+'dd'.join(str(time()).split('.'))
        t = t + '.sdf'
        with open(t,'w') as f: f.write(self.pickup())
