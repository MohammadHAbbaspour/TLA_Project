


class Transition:
    def __init__(self, cs, ra, ns, wa, m):
        self.current_state = f'q{cs}'
        self.read_alpha = '#' if ord(ra) == 96 else ra
        self.next_state = f'q{ns}'
        self.write_alpha = '#' if ord(wa) == 96 else wa
        self.move = m

class Turing:
    def __init__(self):
        self.productions = []
        self.initial_state = None
        self.final_state = None

    def Decode_String(self, string):
        productions = string.split('00')
        for p in productions:
            self.productions.append(self.Decode_Transition(p))

    def Decode_Transition(self, string):
        tr = string.split('0')
        return Transition(tr[0].count('1'), chr(95 + tr[1].count('1')), 
                            tr[2].count('1'), chr(95 + tr[3].count('1')),
                            'L' if tr[4] == '1' else 'R')

    def Decode_Input(self, string):
        result = ''
        string_splitted = string.split('0')
        for s in string_splitted:
            result += '#' if chr(s.count('1')) == 1 else chr(s.count('1') + 95)
        return '#'*len(result) + result + '#'*len(result)

    def state_numbers(self):
        states = set()
        for p in self.productions:
            states.add(p.current_state)
            states.add(p.next_state)
        return len(states)

    def Get_Transition(self, q, read_alpha):
        transition = None
        for tr in self.productions:
            if tr.current_state == q and tr.read_alpha == read_alpha:
                transition = tr
        return transition

    def Halt(self, q, read_alpha, i, n):
        if i == n + 1:
            return True
        transition = self.Get_Transition(q, read_alpha)
        return True if transition is None else False

    def Check_String(self, string):
        tape = self.Decode_Input(string)
        head = int(tape.count('#')/2)
        self.initial_state = 'q1'
        self.final_state = f'q{self.state_numbers()}'
        q = self.initial_state
        n = len(tape) - head
        if tape == '#_#':
            if self.Get_Transition(q, '#') is not None:
                print('Accepted')
            else:
                print('Rejected')
            return
        halt = self.Halt(q, tape[head], head, n)
        while not halt:
            transition = self.Get_Transition(q, tape[head])
            q = transition.next_state if transition is not None else ''
            tape = tape[0 : head] + (transition.write_alpha if transition is not None else tape[head]) + tape[head + 1 ::]
            if transition.move == 'L':
                head -= 1
            else:
                head += 1
            halt = self.Halt(q, tape[head], head, n)
        if q == self.final_state:
            print('Accepted')
        else:
            print('Rejected')


turing_code = input()
n = int(input())
turing = Turing()
turing.Decode_String(turing_code)
for i in range(n):
    string = input()
    turing.Check_String(string)