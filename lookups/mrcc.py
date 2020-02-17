from .. import common
anynum = common.anynum

import copy
#Delimiters and regular expressions specific to psi4
lookup = {
    'program': 'mrcc',
    'generic_delim': {
        'gen':
        '\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*[ -.0-9:]+\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*'
    }
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
    'cis_e': {
        'raw': '[0-9]+[ ]+([-.0-9]+)[ ]+[-.0-9]+[ ]+[-.0-9]+[ ]+[.0-9]+',
        'exc': '[0-9]+[ ]+([-.0-9]+)[ ]+[-.0-9]+[ ]+[-.0-9]+[ ]+[.0-9]+'
    },
    'lr-ccs': {
        'ground': 'Total CCS energy \[au\]:[ ]+([-.0-9]+)',
        'excited': 'Total LR-CCS energy \[au\]:[ ]+([-.0-9]+)',
        'rootnum':
        'Starting right-hand LR-CC iteration for root[ ]+([0-9]+) ...'
    },
    'lr-ccsd': {
        'ground': 'Total CCSD energy \[au\]:[ ]+([-.0-9]+)',
        'excited': 'Total LR-CCSD energy \[au\]:[ ]+([-.0-9]+)',
        'rootnum':
        'Starting right-hand LR-CC iteration for root[ ]+([0-9]+) ...'
    },
    'lr-ccsdt': {
        'ground': 'Total CCSDT energy \[au\]:[ ]+([-.0-9]+)',
        'excited': 'Total LR-CCSDT energy \[au\]:[ ]+([-.0-9]+)',
        'rootnum':
        'Starting right-hand LR-CC iteration for root[ ]+([0-9]+) ...'
    },
    'lr-ccsdtq': {
        'ground': 'Total CCSDTQ energy \[au\]:[ ]+([-.0-9]+)',
        'excited': 'Total LR-CCSDTQ energy \[au\]:[ ]+([-.0-9]+)',
        'rootnum':
        'Starting right-hand LR-CC iteration for root[ ]+([0-9]+) ...'
    },
    'lr-ccsdtqp': {
        'ground': 'Total CCSDTQP energy \[au\]:[ ]+([-.0-9]+)',
        'excited': 'Total LR-CCSDTQP energy \[au\]:[ ]+([-.0-9]+)',
        'rootnum':
        'Starting right-hand LR-CC iteration for root[ ]+([0-9]+) ...'
    },
}

lookup['sections'] = {
    'hf': {
        'start': 'Executing scf...',
        'end': 'RETURNING FROM SCF ALGORITHM'
    },
    'cis_e': {
        'start':
        'Final result of the CIS calculations for the[ a-z]+excited states:',
        'end':
        'Calculate oscillator and rotational strength...'
    },  #this end mark is temporary, I hope
    #as it is now, can't get osc strength
    'cis_prop': {
        'start': 'Final result for the[ a-z]+excited states:',
        'end': 'CPU time \[min\]:[ ]+[.0-9]+[ ]+Wall time \[min\]:[ ]+[.0-9]+'
    },
    'lr-ccs': {
        'start': 'LR-CCS calculation',
        'end': lookup['generic_delim']['gen']
    },
    'lr-ccsd': {
        'start': 'LR-CCSD calculation',
        'end': lookup['generic_delim']['gen']
    },
    'lr-ccsdt': {
        'start': 'LR-CCSDT calculation',
        'end': lookup['generic_delim']['gen']
    },
    'lr-ccsdtq': {
        'start': 'LR-CCSDTQ calculation',
        'end': lookup['generic_delim']['gen']
    },
    'lr-ccsdtqp': {
        'start': 'LR-CCSDTQP calculation',
        'end': lookup['generic_delim']['gen']
    }
}

lookup['properties'] = {'HF': {'diis': 'DIIS ([a-z]+).'}}
