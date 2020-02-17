from .. import common
anynum = common.anynum

#Delimiters and regular expressions specific to CFOUR
lookup = {
    'program': 'cfour',
    'generic_delim': {
        'start': '@GETMEM',
        'end': '@CHECKOUT'
    },
    'exit_controlled': '--executable [ vxe]cc finished with status[ ]+0'
}

lookup['energy'] = {
    'HF': {
        'raw': 'E\(SCF\)=[ ]+' + anynum
    },
    'MP2': {
        'raw': 'Total MP2 energy[ ]+=[ ]+' + anynum
    },
    'CCSD': {
        'raw': 'The total energy is[ ]+' + anynum,
        '(T)': 'CCSD(T) energy[ ]+' + anynum
    }
}

lookup['sections'] = {
    'HF': {
        'start': 'Parameters for SCF calculation:',
        'end': lookup['generic_delim']['end']
    },
    'MP2': {
        'start': 'Second-order MP',
        'end': lookup['generic_delim']['start']
    },
    'CCSD': {
        'start': 'CCSD energy will be calculated',
        'end': lookup['generic_delim']['end']
    }
}

lookup['properties'] = {'HF': {'fin': 'VSCF finished'}}
