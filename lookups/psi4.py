from .. import common
anynum = common.anynum

import copy
#Delimiters and regular expressions specific to psi4
lookup = {
    'program': 'psi4',
    'generic_delim': {
        'end': '\*\*\* tstop\(\) called on',
        'start': '\*\*\* tstart\(\) called on'
    },
    'exit_success': '\*\*\* Psi4 exiting successfully. Buy a developer a beer'
}

#TODO energies: ran enormous number of methods, find correct delims in there

#lookup energies, properties should be regexes that return the value asked for
#lookup section should contain regexes that do not return a value
lookup['energy'] = {
    'HF': {
        'raw': 'Final Energy:[ ]+' + anynum,
        'Nuc': 'Nuclear Repulsion Energy =[ ]+' + anynum,
        '1eE': 'One-Electron Energy =[ ]+' + anynum,
        '2eE': 'Two-Electron Energy =[ ]+' + anynum
    },
    'DFT': {
        'raw': 'Final Energy:[ ]+' + anynum,
        'Nuc': 'Nuclear Repulsion Energy =[ ]+' + anynum,
        '1eE': 'One-Electron Energy =[ ]+' + anynum,
        '2eE': 'Two-Electron Energy =[ ]+' + anynum
    },
    'DFMP2': {
        'raw': '(?<!SCS) Total Energy[ ]+=[ ]+' + anynum
    },
    'MP2': {
        'raw': '(?<!SCS) Total Energy[ ]+=[ ]+' + anynum
    },
    'CCSD': {
        'raw': 'Total CCSD energy[ ]+\(file100\)[ =]+' + anynum,
        'corr': '(?<!Total) CCSD energy[ ]+\(file100\)[ =]+' + anynum,
        'MP2': '\* MP2 total energy[ =]+' + anynum,
        'dMP2': 'MP2 correlation energy[ ]+' + anynum,
        'd(T)': '\(T\) energy[ =]+' + anynum,
        '(T)': '\* CCSD\(T\) total energy[ =]+' + anynum
    },
    'DETCI' : {
        'raw': 'DETCI Root 0 energy =\s+([-.0-9]+)',
        'root': 'DETCI Root [0-9]+ energy =\s+([-.0-9]+)'
    }
}

lookup['sections'] = {
    'GEOM':{
        'start': '==> Geometry <==',
        'end': 'Nuclear'
    },
    'HF': {
        'start': 'HF Reference',
        'end': lookup['generic_delim']['end'],
        'post': '==> Post-Iterations <=='
    },
    'DFT': {
        'start': 'KS Reference',
        'end': 'Computation Completed'
    },
    'opt': {
        'start': '==> Convergence Check <==',
        'end': 'OPTKING Finished Execution'
    },
    'freq': {
        'start': '==> Harmonic Vibrational Analysis <==',
        'end': 'Total G, Free enthalpy'
    },
    'MP2': {
        'start': '2nd-Order Moller-Plesset Theory',
        'end': lookup['generic_delim']['end']
    },
    'DFMP2': {
        'start': '2nd-Order Density-Fitted Moller-Plesset Theory',
        'end': lookup['generic_delim']['end']
    },
    'CCSD': {
        'start': '\*        CCENERGY        \*',
        'end': lookup['generic_delim']['end'] + '|' + lookup['exit_success']
    },
    'DETCI': {
        'start': "D E T C I",
        'end': lookup['generic_delim']['end'] + '|' + lookup['exit_success']
    }
}

lookup['properties'] = {
    'GEOM': {
        'cart':'([A-Z]|[A-Z][A-Z])\s+([-.0-9]+)\s+([-.0-9]+)\s+([-.0-9]+)\s+'#([-.0-9]+)'
        },
    'HF': {
        'diis': 'DIIS ([a-z]+).',
        'mom': 'MOM ([a-z]+).',
        'frac': 'Fractional occupation ([a-z]+).',
        'guess': 'Guess Type is ([A-Za-z0-9]+)',
        'basis': 'Basis Set: ([A-Za-z0-9]+)',
        'alg': 'SCF Algorithm Type is ([A-Za-z]+)'
    },  #,
    #'post':
    #{'orbital_energies':'[ ]+([1-9A-Z]+)[]+([-.0-9]+)'}},
    'DFT': {
        'diis': 'DIIS ([a-z]+).',
        'mom': 'MOM ([a-z]+).',
        'frac': 'Fractional occupation ([a-z]+).',
        'guess': 'Guess Type is ([A-Za-z0-9]+)',
        'basis': 'Basis Set: ([A-Za-z0-9]+)',
        'alg': 'SCF Algorithm Type is ([A-Za-z]+)'
    },  #,
    #'post':
    #{'orbital_energies':'[ ]+([1-9A-Z]+)[]+([-.0-9]+)'}}
    'opt': {
        'iteration':
        '[ ]+([0-9]+)[ ]+([\\+-e.0-9]+)[ o\*]+([\\+-e.0-9]+)[ o\*]+([\\+-e.0-9]+)[ o\*]+([\\+-e.0-9]+)[ o\*]+([\\+-e.0-9]+)[ o\*]+',
        'summary':
        '[ ]+([0-9]+)[ ]+([-.0-9]+)[ ]+([-.0-9]+)[ ]+([-.0-9]+)[ ]+([-.0-9]+)[ ]+([-.0-9]+)',
        'entry':
        ' ([A-Za-z]+)[ ]+([-.0-9]+)[ ]+([-.0-9]+)[ ]+([-.0-9]+)',
        'success':
        'Optimization is complete!'
    },
    'freq': {
        'entry':
        'Freq \[cm\^-1\][ ]+([-.0-9i]+)[ ]+([-.0-9i]+)[ ]+([-.0-9i]+)',
        'zpve': 'Total ZPE, Electronic energy at 0 \[K\][ ]+([-.0-9]+)'
    }
}
#add aliases
#lookup['energy']['HF'] = copy.deepcopy(lookup['energy']['SCF']['raw'])
#lookup['energy']['DFT'] = copy.deepcopy(lookup['energy']['SCF']['raw'])
