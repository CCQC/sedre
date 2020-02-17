from .. import common
anynum = common.anynum

#Delimiters and regular expressions specific to Molpro
lookup = {'program':'molpro',
                                       'generic_delim':"\*"*80,
                                       'opt_done_delim':"END OF GEOMETRY OPTIMIZATION",
                                       'geom_entry':'( ([0-9A-Z=]+)[ ]+([-.0-9]+)([ A-Z]+))+',
                                       'exit_controlled':'Variable memory released'}

#I believe these are unique regexes for energies !within! the relevant sections
lookup['energy']={'MRCI':{'raw' :'MRCI STATE [.0-9] Energy[ ]+([-.0-9]+)',
                        'reference':'Reference energy[ ]+([-.0-9]+)',
                        'corrected':\
                                    {'davidson':
                                    {'fixed':'Cluster corrected energies[ ]+([-.0-9]+) \(Davidson, fixed reference\)',
                                    'relaxed':'Cluster corrected energies[ ]+([-.0-9]+) \(Davidson, relaxed reference\)'},
                                    'pople':\
                                    {'fixed':'Cluster corrected energies[ ]+([-.0-9]+)',
                                    'relaxed':'Cluster corrected energies[ ]+([-.0-9]+)'}
                            }},
                  'RHF':{'raw':'\!RHF STATE[ .0-9]+Energy[ ]+([-.0-9]+)',
                         'sub1':{'raw':'\!RHF STATE[ .0-9]+Energy[ ]+([-.0-9]+)'}},
                  'MULTI':{'raw':'\!MCSCF STATE[ .0-9]+Energy[ ]+([-.0-9]+)'},
                  'RS2':{'raw':'\!RSPT2 STATE[ .0-9]+Energy[ ]+([-.0-9]+)'},
                  'CCSD':{'U':{'singles':'UCCSD singles energy[ ]+([-.0-9]+)',
                                'pair':'UCCSD pair energy[ ]+([-.0-9]+)',
                                'correlation':'UCCSD correlation energy[ ]+([-.0-9]+)',
                                'raw':'RHF-UCCSD energy[ ]+([-.0-9]+)',
                                '(T)':'RHF-UCCSD\(T\) energy[ ]+([-.0-9]+)',
                                '[T]':'RHF-UCCSD\[T\] energy[ ]+([-.0-9]+)',
                                '-T':'RHF-UCCSD-T energy[ ]+'+anynum},
                                'RMP2':{'raw':'!*RHF-RMP2 energy[ ]+([-.0-9]+)'}}}
lookup['delimiters']={'geometry':{'cart':{'start':'Current geometry \(xyz format, in Angstrom\)',
                                         'end':lookup['generic_delim']},
                                 'zmat':{'start':'Variable[ ]+Last[ ]+Current[ ]+Next[ ]+Gradient[ ]+Hessian[ ]+',
                                         'end':'Convergence:'}}}
lookup['properties']={'geometry':{'zmat':
                                        {'connectivity':{'start':'geometry={','end':'}'},
                                         'vals':'( ([0-9A-Z=]+)      ([-.0-9]+)([ A-Z]+))+'}},
                      #'civecs':{'raw':" ([012ab]+)[ ]+([-.0-9]+)"},
                      'MULTI':{'civecs':{'raw':" ([012ab]+)[ ]+([-.0-9]+)\n"}},
                      'MRCI':{'raw':None}}
                              #'ci_vectors':{'start':'CI vector','end':lookup['generic_delim'],
                               #             'vals':" ([012ab]+)[ ]+([-.0-9]+)"}}

lookup['sections']={'RHF':{'start':'PROGRAM \* RHF-SCF',
                            'end':lookup['generic_delim'],
                            'sub1':{'start':'PROGRAM \* RHF-SCF',
                                   'end':lookup['generic_delim']}},
                    'civecs':{'start':'CI vector','end':lookup['generic_delim']},
                    'MULTI':{'start':'PROGRAM \* MULTI',
                            'end':lookup['generic_delim'],
                            'civec':{'start':'CI vector',
                                     'end':'TOTAL ENERGIES'}},
                    'RS2':{'start':'1PROGRAM \* RS2 \(Multireference RS Perturbation Theory\)',
                           'end':lookup['generic_delim']},
                    'MRCI':{'start':'PROGRAM \* CI \(Multireference',
                    'end':lookup['generic_delim']}} #add CC section!
