import re

operators = ['=', '+', '-', '*', '/', '<', '>', '==', '!=', 'from', 'to', 'do', 'return', 'if', 'else', 'end', 'var']
numerals = r'[0-9]+'
variable_usage = r''
prohibited = ['!', '@', '#', '&', '\\', '.', '\n']
codes = [operators[0], operators[1], operators[2], operators[3],
         operators[4], operators[5], operators[6], operators[7],
         operators[8], operators[9], operators[10], operators[11],
         operators[12], operators[13], operators[14], operators[15], operators[16],
         'id', 'con', ';']
statement = [operators[11], operators[13]]
mathematical_operators = [operators[1], operators[2], operators[3], operators[4]]
simple_math_expr = re.compile(r"\s*[=]\s*[\w+]\s*[+|-|*|\/]\s*\w+")

variables_declaration = re.compile(r"var\s\w+\s*[=]\s*[\d|\w]+\s*[;]")
logical_statement = re.compile(re.escape(variable_usage) + r"\s" + r"<|>" + r"\s" + re.escape(variable_usage))
if_statement = re.compile(r"if\s\w+\s[<|>]\s\w+\s*")
assignment = re.compile(r"\w+\s*[=]\s*")
logical_operators = [operators[5], operators[6], operators[7], operators[8]]
