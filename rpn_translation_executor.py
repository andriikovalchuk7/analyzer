
LEFT_ASSOC = 0
RIGHT_ASSOC = 1

OPERATORS = {
    '(': (0, LEFT_ASSOC),
    'if': (0, LEFT_ASSOC),
    'iterate': (0, LEFT_ASSOC),
    ')': (2, LEFT_ASSOC),
    'finish': (2, LEFT_ASSOC),
    '=': (3, LEFT_ASSOC),
    'var': (4, LEFT_ASSOC),
    '<': (5, LEFT_ASSOC),
    '>': (5, LEFT_ASSOC),
    '<=': (5, LEFT_ASSOC),
    '>=': (5, LEFT_ASSOC),
    '!=': (5, LEFT_ASSOC),
    '+': (6, LEFT_ASSOC),
    '-': (6, LEFT_ASSOC),
    '*': (8, LEFT_ASSOC),
    '/': (8, LEFT_ASSOC),
    '%': (8, LEFT_ASSOC),
    '^': (10, RIGHT_ASSOC)
}

def isOperator(token):
    return token in OPERATORS.keys()


def isAssociative(token, assoc):
    if not isOperator(token):
        raise ValueError('Invalid token: %s' % token)
    return OPERATORS[token][1] == assoc


def cmpPrecedence(token1, token2):
    if not isOperator(token1) or not isOperator(token2):
        raise ValueError('Invalid tokens: %s %s' % (token1, token2))
    return OPERATORS[token1][0] - OPERATORS[token2][0]


def infixToRPN(tokens):
    out = []
    stack = []
    for token in tokens:
        if token == ';':
            continue
        if isOperator(token):
            while len(stack) != 0 and isOperator(stack[-1]):
                if (isAssociative(token, LEFT_ASSOC)
                    and cmpPrecedence(token, stack[-1]) <= 0) or (isAssociative(token, RIGHT_ASSOC)
                     and cmpPrecedence(token, stack[-1]) < 0):
                    out.append(stack.pop())
                    continue
                break
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while len(stack) != 0 and stack[-1] != '(':
                out.append(stack.pop())
            stack.pop()
        else:
            out.append(token)
        print(stack)
    while len(stack) != 0:
        out.append(stack.pop())
    return out


if __name__ == '__main__':
    #input = "1 + 2 * ( 3 / 4 ) ^ ( 5 + 6 )".split(" ")
    input = "var a = 10 ; " \
            "iterate a times " \
            "if a < 109 " \
            "a = a + 111 ; " \
            "else " \
            "var z = 10 ; " \
            "end ; " \
            "finish " \
            "var za = 10 ; "
    input = input.split(" ")
    output = infixToRPN(input)
    print(output)