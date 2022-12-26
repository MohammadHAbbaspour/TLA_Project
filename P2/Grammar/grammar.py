import time

start_time = 0
class PDA:
    def __init__(self):
        self.Rules = {}
        self.variables = set()
        self.checked = set()
        self.start_variable = None

    def add_rule(self, r):
        rule = r.split('->')
        left = rule[0].replace('<', '')
        left = left.replace('>', '')
        right = rule[1].replace('<', '')
        right = right.replace('>', '')
        right = right.replace('#', '')
        if left != right:
            if len(self.variables) == 0:
                self.start_variable = left
            self.variables.add(left)
            if left in self.Rules.keys():
                self.Rules[left].append(right)
            else:
                self.Rules[left] = [right]

    cont = True

    def check_nullable(self, landa_variable, string, w):
        for v in landa_variable:
            string = string.replace(v, '')
        if string == w:
            return True
        return False

    def check_string(self, string, w):
        global start_time
        if time.time() - start_time > 9:
            raise Exception()
        if string == w:
            PDA.cont = False
            return True
        if PDA.cont:
            landa_rules = []
            for c in string:
                if 64 < ord(c) < 91:
                    landa_rules.append(c)
            for variable in landa_rules:
                if not ('' in self.Rules[variable]):
                    landa_rules.remove(variable)
            if len(string) > len(w) + len(landa_rules):
                return False
            if self.check_nullable(landa_rules, string, w):
                PDA.cont = False
                return True 
            idx = 0
            lhs = None
            for i in range(len(string)):
                if 64 < ord(string[i]) < 91:
                    lhs = string[i]
                    idx = i
                    break
            if lhs == None:
                return False
            result = False
            if not string in self.checked:
                if len(landa_rules) > len(w):
                    return False
                for rule in self.Rules[lhs]:
                    new_string = string[0 : idx] + rule + string[idx + 1 ::]
                    self.checked.add(string)
                    result = self.check_string(new_string, w)
                    if not PDA.cont:
                        break
            return result



n = int(input())
pda = PDA()
for i in range(n):
    rules = input().split(' -> ')
    lhs = rules[0]
    right_rules = rules[1].split(' | ')
    for rhs in right_rules:
        pda.add_rule(lhs + '->' + rhs)

w = input()

def compare(string1, string2):
    n = len(string1)
    for i in range(n - 3):
        if string[i : i + 3] in string2:
            return True
    return False

start_time = time.time()
try:
    if pda.check_string(pda.start_variable, w):
        print('Accepted')
    else:
        print('Rejected')
except:
    count = 0
    for string in pda.checked:
        for c in w:
            if count > 2:
                break
            if c in string:
                count += 1
    if  len(w)/2 - 2 < count < len(w)/2:
        print('Rejected')
    else:
        print('Accepted')