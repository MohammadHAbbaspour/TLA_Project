
class PDA:
    def __init__(self):
        self.Rules = {}
        self.variables = set()
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
        stack = []
        stack.append(string)
        while len(stack) > 0:
            string = stack.pop()
            if string == w:
                return True
            landa_rules = []
            for c in string:
                if 64 < ord(c) < 91:
                    landa_rules.append(c)
            for variable in landa_rules:
                if not ('' in self.Rules[variable]):
                    landa_rules.remove(variable)
            if len(string) > len(w) + len(landa_rules):
                continue
            if self.check_nullable(landa_rules, string, w):
                return True
            idx = 0
            lhs = None
            for i in range(len(string)):
                if 64 < ord(string[i]) < 91:
                    lhs = string[i]
                    idx = i
                    break
            if lhs == None:
                continue
            for rule in self.Rules[lhs]:
                new_string = string[0 : idx] + rule + string[idx + 1 ::]
                stack.append(new_string)
        return False



n = int(input())
pda = PDA()
for i in range(n):
    rules = input().split(' -> ')
    lhs = rules[0]
    right_rules = rules[1].split(' | ')
    for rhs in right_rules:
        pda.add_rule(lhs + '->' + rhs)

w = input()


# try:
if pda.check_string(pda.start_variable, w):
    print('Accepted')
else:
    print('Rejected')
# except:
#     print('Accepted')