operators = ['=', '+', '-', '*', '/', '<', '>', '==', '!=', 'iterate', 'times', 'finish', 'return', 'if', 'else', 'end', 'var']
variable_usage = r'[a-zA-Z]'
prohibited = ['!', '@', '#', '&', '\\', '.', '\n']
codes = [operators[0], operators[1], operators[2], operators[3],
         operators[4], operators[5], operators[6], operators[7],
         operators[8], operators[9], operators[10], operators[11],
         operators[12], operators[13], operators[14], operators[15], operators[16],
         'id', 'con', ';']
statement = [operators[11], operators[13]]
mathematical_operators = [operators[1], operators[2], operators[3], operators[4]]
logical_operators = [operators[5], operators[6], operators[7], operators[8]]
