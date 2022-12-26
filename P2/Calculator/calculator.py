import math
import decimal


class Calculator:
    precedence = {'^' : 4, '*' : 3, '/' : 3, '+' : 2, '-' : 2, '(' : 1}
    def __init__(self, expression):
        self.expression = expression

    def is_number(self, expr):
        try:
            decimal.Decimal(expr)
            return True
        except:
            return False

    def is_operator(self, char):
        if char == '*' or char == '/' or char == '+' or char == '-' or char == '^':
            return True
        return False

    def is_operand(self, token):
        return self.is_number(token)

    def is_function(self, expr):
        if (expr in 'abs') or (expr in 'sqrt') or (expr in 'sin') or (expr in 'cos') or (expr in 'tan') or (expr in 'ln') or (expr in 'exp') or ('ln' in expr):
            return True
        return False

    def compare_precedence(self, operator1, operator2):
        '''compare precedence between two operands'''
        if Calculator.precedence[operator1] > Calculator.precedence[operator2]:
            return True
        return False

    def calculate_function(self, fun, input):
        if fun == 'abs':
            return abs(decimal.Decimal(input))
        if fun == 'sqrt':
            return math.sqrt(decimal.Decimal(input))
        if fun == 'sin':
            return math.sin(decimal.Decimal(input))
        if fun == 'cos':
            return math.cos(decimal.Decimal(input))
        if fun == 'tan':
            return math.tan(decimal.Decimal(input))
        if fun == 'ln':
            return math.log(decimal.Decimal(input), math.e)
        if fun == 'exp':
            return math.exp(decimal.Decimal(input))
        if fun == '':
            return decimal.Decimal(input)

    def calculate_math_expression(self, l, r, fun) -> float:
        '''get the left_hand_side and right_hand_side of a math main operand then return the result'''
        if fun == '+':
            return str(decimal.Decimal(l) + decimal.Decimal(r))
        elif fun == '-': 
            return str(decimal.Decimal(l) - decimal.Decimal(r))
        elif fun == '*':
            return str(decimal.Decimal(l) * decimal.Decimal(r))
        elif fun == '/':
            return str(decimal.Decimal(l) / decimal.Decimal(r))
        elif fun == '^':
            return str(decimal.Decimal(l) ** decimal.Decimal(r))

    def calculate(self, expression : list):
        '''return the result of a simple math expression (with only digits and operands => 2 + 3 * 5 / 5)\n
            first convert to postfix expression then calculate it.'''
        postfix = ''
        stack = []
        for token in expression:
            if self.is_operand(token):
                postfix += token + ' '
            elif token == '(':
                stack.append(token)
            elif token == ')':
                top = stack.pop()
                while top != '(':
                    postfix += top + ' '
                    top = stack.pop()
            elif self.is_operator(token):
                if not len(stack):
                    stack.append(token)
                else:
                    top = stack[len(stack) - 1]
                    if self.is_operator(top) or top == '(':
                        if self.compare_precedence(token, top):
                            stack.append(token)
                        else:
                            while not self.compare_precedence(token, top) or not len(stack):
                                postfix += top + ' '
                                stack.pop()
                                top = stack[len(stack) - 1] if len(stack) else ''
                                if not self.is_operator(top):
                                    break
                            stack.append(token)
        while len(stack):
            postfix += stack.pop() + ' '
        postfix = postfix[0 : len(postfix) - 1]
        return self.calculate_postfix(postfix.split(' '))

    def calculate_postfix(self, postfix) -> str:
        '''return the result of a postfix expression'''
        stack = []
        for token in postfix:
            if self.is_operand(token):
                stack.append(token)
            else:
                r = stack.pop()
                l = stack.pop()
                stack.append(str(self.calculate_math_expression(l, r, token)))
        if len(stack) > 1:
            raise Exception()
        return stack.pop()

    def check_valid(self, expression):
        stack = []
        for token in expression:
            if token == '(':
                stack.append(token)
            elif token == ')':
                stack.pop()
        if len(stack) > 0:
            raise Exception()

    def find_functions(self, i, expr):
        fun = ''
        while expr[i] != '(':
            fun += expr[i]
            i += 1
        if i == len(expr):
            raise Exception()
        open_parentheses = 1
        j = i + 1
        while open_parentheses > 0 and j < len(expr):
            if expr[j] == '(':
                open_parentheses += 1
            if expr[j] == ')':
                open_parentheses -= 1
            j += 1
        if open_parentheses != 0:
            raise Exception()
        return fun, j - 1

    def calculate_expression(self, expression):
        self.check_valid(expression)
        string = ''
        i = 0
        while i < len(expression) - 1:
            if (expression[i] == '(') or self.is_function(expression[i : i + 2]):
                function, j = self.find_functions(i, expression)
                input = expression[i + len(function) + 1 : j]
                result = self.calculate_expression(input)
                string += str(self.calculate_function(function, result))
                i = j + 1
            else:
                string += expression[i]
                i += 1
        string += expression[len(expression) - 1] if i < len(expression) else ''
        return self.calculate(string.split(' '))

expression = input()
calculator = Calculator(expression)
try:
    first_result = str("%f" %decimal.Decimal(calculator.calculate_expression(expression)))
    final_result = ''
    i = 0
    if not '.' in first_result:
        first_result += '.0'
    while first_result[i] != '.':
        final_result += first_result[i]
        i += 1
    final_result += first_result[i]
    final_result += first_result[i + 1]
    i += 2
    if i == len(first_result):
        final_result += '0'
    else:
        final_result += first_result[i]
    if len(final_result[0 : i - 2]) == final_result[0 : i - 2].count('0'):
        final_result = final_result[max(i - 3, 0) ::]
    print(final_result)
except :
    print('INVALID')

