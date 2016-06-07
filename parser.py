import re

esc = chr(0x1B)
endl = esc + '[m'
color = {'BR': esc + '[0;31m',
         'B': esc + '[0;31m',
         'G': esc + '[0;32m',
         'O': esc + '[0;33m',
         'OT': esc + '[0;33m',
         'R': esc + '[1;31m',
         'BL': esc + '[1;34m',
         'T': esc + '[0;30;47m'}

class Line(object):
    def __new__ (self, str):
        if str.count(',') != 6 : return None
        else: return object.__new__(self)
    
    def __init__ (self, str):
        #print >> sys.stderr, str
        str_sp = str.split(',')
        self.num = str_sp[0]
        self.name = str_sp[1]
        
        self.m_p_s = str_sp[5]
        self.m_p = float(self.m_p_s[:-1])
        self.y_p_s = str_sp[6]
        self.y_p = float(self.y_p_s[:-1])
        
        tmp = str_sp[2].strip()
        if len(tmp) > 3: self.now = tmp[:-3] + ',' + tmp[-3:]
        else: self.now = tmp
        tmp = str_sp[3].strip()
        if len(tmp) > 3: self.month = tmp[:-3] + ',' + tmp[-3:]
        elif len(tmp) == 1:
            self.month = ' '
            self.m_p_s = '  NEW  '
            self.m_p = 10001.0
        else: self.month = tmp
        tmp = str_sp[4].strip()
        if len(tmp) > 3: self.year = tmp[:-3] + ',' + tmp[-3:]
        elif len(tmp) == 1:
            self.year = ' '
            self.y_p_s = '  NEW  '
            self.y_p = 10001.0
        else: self.year = tmp
    
    def output (self):
        out = ''
        
        def colour (pp):
            return color[re.findall('^[a-zA-Z]+', pp)[0]]
        
        self.no = self.num.split('/')
        self.color = list()
        
        for i in self.no: self.color.append(colour(i))
        
        if len(self.no) == 2:
            ab = self.color[0] + self.no[0] + esc + '[1;37m/' + endl
            ab += self.color[1] + self.no[1] + endl
            out += ab + ' ' * (9 - len(self.num))
            ab = self.color[0] + self.name[0:len(self.name) / 2]
            ab += self.color[1] + self.name[len(self.name) / 2:] + endl
            out += ab + ' ' * (16 - len(self.name))
        else:
            if re.search('^[tT][0-9]+', self.no[0]) is None:
                out += self.color[0] + self.num
                out += ' ' * (9 - len(self.num))
            else:
                out += ' ' * 9 + self.color[0]
            out += self.name + endl + ' ' * (16 - len(self.name))
            
        out += ' ' * (7 - len(self.now)) + self.now
        out += ' ' * (8 - len(self.month)) + self.month
        out += ' ' * (8 - len(self.year)) + self.year
        
        out += ' ' * (8 - len(self.m_p_s))
        if self.m_p >= 1000: out += esc + '[1;37;43m'
        elif self.m_p >= 50: out += esc + '[1;37;45m'
        elif self.m_p >= 10: out += esc + '[1;37;41m'
        elif self.m_p >= 1: out += esc + '[1;31;40m'
        elif -1 < self.m_p < 1: out += esc + '[1;37;40m'
        elif self.m_p > -10: out += esc + '[1;32;40m'
        elif self.m_p > -50: out += esc + '[1;37;42m'
        else: out += esc + '[1;37;46m'
        out += self.m_p_s
        
        out += esc + '[m' + ' ' * (8 - len(self.y_p_s))
        if self.y_p >= 1000: out += esc + '[1;37;43m'
        elif self.y_p >= 50: out += esc + '[1;37;45m'
        elif self.y_p >= 10: out += esc + '[1;37;41m'
        elif self.y_p >= 1: out += esc + '[1;31;40m'
        elif -1 < self.y_p < 1: out += esc + '[1;37;40m'
        elif self.y_p > -10: out += esc + '[1;32;40m'
        elif self.y_p > -50: out += esc + '[1;37;42m'
        else: out += esc + '[1;37;46m'
        out += self.y_p_s + esc + '[m'
        
        print(out)

def parse(file):
    i = 1
    last = -1
    reading = file.split('\n')
    for l in reading:
        tmp = Line(l)
        if tmp == None: break
        if last == tmp.now : print ' ' * 4,
        else : print str(i) + ' ' * (4 - len(str(i))),
        last = tmp.now
        tmp.output()
        if i % 5 == 0: print ''
        i += 1

def main(filename):
    import os
    if os.path.exists(filename):
        input = ''
        try:
            with open(filename) as file:
                input = input + file.read()
        except IOError:
            print('failed to open ' + filename + '!')
            return
        except:
            print('some unknown error!')
            return
        parse(input)
    else: print(filename + ' not found!')

if __name__ == '__main__' :
    import sys
    
    if(len(sys.argv) == 1): print('please add file name as argument!')
    elif(len(sys.argv) > 2): print('too many arguments!')
    else: main(sys.argv[1])
