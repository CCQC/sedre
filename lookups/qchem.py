from .. import common
anynum = common.anynum

#Delimiters and regular expressions specific to Q-Chem (written for 5.X)
lookup = {
    'program': 'qchem',
    'generic_delim': {
        'gen': '-------------------------------------------------------'
    }
}

lookup['energy'] = {
    'HF': {
        'raw': 'SCF[ ]+energy in the final basis set[ =]+' + anynum
    },
    'CIS': {
        'raw': 'Total energy for state[ 0-9\:]+([-.0-9]+)',
        'exc': 'Excited state[ 0-9\:]+excitation energy \(eV\)[ =]+([-.0-9]+)'
    },
    'TDDFT': {
        'raw': 'Total energy for state[ 0-9\:]+([-.0-9]+)',
        'exc': 'Excited state[ 0-9\:]+excitation energy \(eV\)[ =]+([-.0-9]+)'
    },
    'EOM': {
        'raw':
        'Total energy = ([-.0-9]+) a.u.  Excitation energy = [-.0-9]+ eV.',
        'exc':
        'Total energy = [-.0-9]+ a.u.  Excitation energy = ([-.0-9]+) eV.'
    }
}

lookup['properties'] = {
    'CIS': {
        'mult': 'Multiplicity\: ([A-Za-z]+)',
        'str': 'Strength[ \:]+([-.0-9]+)'
    },
    'orbitals': {
        'alpha': {
            'occ': {
                'e': '\s*([-0-9]+.[0-9]+(?!=.*[A-Za-z]))'
            },
            'vir': {
                'e': '\s*([-0-9]+.[0-9]+(?!=.*[A-Za-z]))'
            }
        },
        'beta': {
            'occ': {
                'e': '\s*([-0-9]+.[0-9]+(?!=.*[A-Za-z]))'
            },
            'vir': {
                'e': '\s*([-0-9]+.[0-9]+(?!=.*[A-Za-z]))'
            }
        }
    },
    'TDDFT': {
        'mult': 'Multiplicity\: ([A-Za-z]+)',
        'str': 'Strength[ \:]+([-.0-9]+)',
        'pg': 'Molecular Point Group[ ]+([A-Za-z0-9]+)[ A-Za-z0-9=]+',
        'trans_sym': []
    },
    'EOM': {
        'sym': 'EOM[A-Z]+ transition [0-9]+/([0-9ABgu\'\"]+)'
    }
}
#add EOM

lookup['sections'] = {
    'HF': {
        'start': 'Hartree-Fock SCF calculation will be',
        'end': 'Total energy in the final basis set'
    },
    'CIS(D)': {
        'start': 'Solving for CISD [A-Z]+ transitions.',
        'end': 'CISD computation'
    },
    'CIS': {
        'start': '<FULL> \'N; /CIS Excitation Energies[ \s]+/{n;n;=}\'',
        'end': lookup['generic_delim']['gen']
    },
    'TDDFT': {
        'start':
        '<FULL>M|2 \'N; /Molecular Point Group[ ]+[A-Za-z0-9]+[ A-Za-z0-9=]+/{=}\'',
        'end':
        'Ground-State Mulliken Net Atomic Charges',
        'occ_orbitals': {
            'start': '<FULL> \'N; /Alpha MOs, Restricted/{n;=}\'',
            'end': '-- Virtual --'
        },
        'vir_orbitals': {
            'start': '-- Virtual --',
            'end': '<FULL>M|2 \'N; /Beta MOs, Restricted/{=}\''
        },
        'transition': {
            'start':
            '<FULL>M|1 \'N; /Excited state[ 0-9\:]+ excitation energy \(eV\) =[ 0-9.]+/{=}\'',
            'end':
            '<FULL> \'N; /D\([ 0-9]+\) --> V\([ 0-9]+\) amplitude = [0-9 .]+/{=}\''
        }
    },
    'orbitals': {
        'start':
        '<FULL> \'N; /Orbital Energies \(a.u.\) and Symmetries/{n;=}\'',
        'end': lookup['generic_delim']['gen'],
        'alpha': {
            'start': '<FULL>M|1 \'N; /Alpha MOs, Restricted/{n;=}\'',
            'end': '<FULL>M|2 \'N; /Beta MOs, Restricted/{=}\'',
            'occ': {
                'start': '<FULL> \'N; /Alpha MOs, Restricted/{n;=}\'',
                'end': '-- Virtual --'
            },
            'vir': {
                'start': '-- Virtual --',
                'end': '<FULL>M|2 \'N; /Beta MOs, Restricted/{=}\''
            }
        },
        'beta': {
            'start': '<FULL>M|2 \'N; /Beta MOs, Restricted/{=}\'',
            'end': lookup['generic_delim']['gen'],
            'occ': {
                'start': '<FULL>M|2 \'N; /Beta MOs, Restricted/{=}\'',
                'end': '-- Virtual --'
            },
            'vir': {
                'start': '-- Virtual --',
                'end': lookup['generic_delim']['gen']
            }
        }
    },
    'EOM': {
        'start': '<FULL>M|2 \'N; /EOMEE transition [0-9/A-Za-z]+/{=}\'',
        'end': 'Summary of significant orbitals\:'
    }
}
