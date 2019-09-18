from collections import namedtuple

Operands_tuple = namedtuple('OpInfo', 'prec assoc')
L, R = 'Left Right'.split()

operands = {
    '^': Operands_tuple(prec=4, assoc=R),
    '=': Operands_tuple(prec=1, assoc=L),
    '*': Operands_tuple(prec=3, assoc=L),
    '/': Operands_tuple(prec=3, assoc=L),
    '+': Operands_tuple(prec=2, assoc=L),
    '-': Operands_tuple(prec=2, assoc=L),
    '(': Operands_tuple(prec=5, assoc=L),
    'var': Operands_tuple(prec=6, assoc=R),
    ')': Operands_tuple(prec=0, assoc=L),
}

number, LPAREN, RPAREN = 'NUMBER ( )'.split()


def get_input(input):
    if input is None:
        input = input('expression: ')
    tokens = input.strip().split()
    tokenvals = []
    for token in tokens:
        if token in operands:
            tokenvals.append((token, operands[token]))
        else:
            tokenvals.append((number, token))
    return tokenvals


def shunting(token_values):
    output, stack = [], []
    table = ['TOKEN,ACTION,RPN OUTPUT,OP STACK,NOTES'.split(',')]
    for token, value in token_values:
        note = action = ''
        if token is number:
            action = 'Add number to output'
            output.append(value)
            table.append((value, action, ' '.join(output), ' '.join(s[0] for s in stack), note))
        elif token in operands:
            token_first, (priority_1, associativity_1) = token, value
            v = token_first
            note = 'Pop ops from stack to output'
            while stack:
                token_2, (priority_2, associativity_2) = stack[-1]
                if (associativity_1 == L and priority_1 <= priority_2) or (associativity_1 == R and priority_1 < priority_2):
                    if token_first != RPAREN:
                        if token_2 != LPAREN:
                            stack.pop()
                            action = '(Pop op)'
                            output.append(token_2)
                        else:
                            break
                    else:
                        if token_2 != LPAREN:
                            stack.pop()
                            action = '(Pop op)'
                            output.append(token_2)
                        else:
                            stack.pop()
                            action = '(Pop & discard "(")'
                            table.append((v, action, ' '.join(output), ' '.join(s[0] for s in stack), note))
                            break
                    table.append((v, action, ' '.join(output), ' '.join(s[0] for s in stack), note))
                    v = note = ''
                else:
                    note = ''
                    break
                note = ''
            note = ''
            if token_first != RPAREN:
                stack.append((token, value))
                action = 'Push op token to stack'
            else:
                action = 'Discard ")"'
            table.append((v, action, ' '.join(output), ' '.join(s[0] for s in stack), note))
    note = 'Drain stack to output'
    while stack:
        v = ''
        token_2, (priority_2, associativity_2) = stack[-1]
        action = '(Pop op)'
        stack.pop()
        output.append(token_2)
        table.append((v, action, ' '.join(output), ' '.join(s[0] for s in stack), note))
        v = note = ''
    return table


if __name__ == '__main__':
    infix = 'var f = a * c ^ k / p - q * g ^ ( n - b ) '
    print('For expression: %r\n' % infix)
    rp = shunting(get_input(infix))
    maxcolwidths = [len(max(x, key=len)) for x in zip(*rp)]
    row = rp[0]
    print(' '.join('{cell:^{width}}'.format(width=width, cell=cell) for (width, cell) in zip(maxcolwidths, row)))
    for row in rp[1:]:
        print(' '.join('{cell:<{width}}'.format(width=width, cell=cell) for (width, cell) in zip(maxcolwidths, row)))
    print('\n The final output RPN is: %r' % rp[-1][2])
