import subprocess as sp
#Common regex patterns
anynum = '([-.0-9]+)'

#Common commands for sed
sed_wrapper = "\'/{}/=\'"
sed_command = "sed -En {} {}"
sed_range_command = "sed -n {},{}p {}"

#Global functions
def call(commandstr,echo=True,do_shell=True,encoding='utf-8'):
    if not echo:
        sp.call(commandstr,shell=do_shell)
        return
    else:
        output = sp.run(commandstr,stdout=sp.PIPE,stderr=sp.PIPE,shell=do_shell)
        if output.returncode != 0:
            return ''
        return(output.stdout.decode(encoding))
    
def line_num(tempstr,file):
    if '<FULL>' in tempstr.split()[0]:
        searchstrin = ' '.join(tempstr.split()[1:])
        full=True
        searchstr=searchstrin
        if 'M' in tempstr.split()[0] and full:
            line_mod = -1*int(tempstr.split()[0].split('|')[-1])
        elif 'P' in tempstr.split()[0] and full:
            line_mod = +1*int(tempstr.split()[0].split('|')[-1])
        else:
            line_mod = 0
    else:
        line_mod = 0
        searchstrin = tempstr
        full=False
        searchstr=sed_wrapper.format(searchstrin)

    lines = call(sed_command.format(searchstr,file)).strip().split('\n')
    if len(lines) < 2 and lines[0] == '':
        return None
    else:
        return [item+line_mod for item in list(map(int,lines))]

def lines_between(line1,line2,file):
    return call(sed_range_command.format(line1,line2,file))

def parse_between(str1,str2,file):
    blocks = [] #list of text blocks that gets returned
    str1_lines = line_num(str1,file)
    str2_lines = line_num(str2,file)
    for idx,val in enumerate(str1_lines):
        for idx2,val2 in enumerate(str2_lines[idx:]):
            if val2 > val:
                #str1_lines[idx] is the same as val, but this is clearer
                blocks.append(lines_between(val,val2,file))
                break
    return blocks

def to_num(r,dihed):
    num = ((r - 1.5)/0.05)*24
    num += dihed/15. + 1
    return num, round(num)

def from_num(num):
    r = (num - (num%24))/24*0.05 + 1.5
    d = ((num - (((r - 1.5)/0.05)*24) - 1)*15)
    return[r,d]
