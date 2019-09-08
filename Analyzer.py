import re
import operators as op
import SyntaxAnalyzer as sa
import csv
from pyexcel.cookbook import merge_all_to_a_book

import glob

array_lexems = [['Row', 'Substring', 'Code', 'Index']]
array_identifiers = [['Index', 'Name', 'Type']]
array_consts = [['Index', 'Const']]


def parse(file):
    text = file.read()
    program = text.split('\n')
    current_row = 0
    identifier_hash = []
    const_hash = []
    lexem_hash = []
    codes_list = merge_codes()
    delimiter = False
    for row in program:
        current_row = current_row + 1
        row = check_if_delimiter_presented(row)
        if row is False:
            return print('Missing end of line token on row %d', current_row)
        delimiter = True
        lexems = re.split(codes_list, row)
        row_number = str(current_row)
        for lexem in lexems:
            lexem = lexem.strip(' ')
            if check_for_prohibits(lexem) is False:
                print('Unexpected token on row %d', current_row)
                return
            if lexem == '':
                continue
            else:
                if op.operators.count(lexem) != 0:
                    lexem_hash.append([row_number, lexem, str(op.codes.index(lexem)), ' '])
                    continue
                if re.match(op.numerals, lexem):
                    id = identifier_id(const_hash, lexem)
                    const_hash.append([id, lexem])
                    lexem_hash.append([row_number, lexem, str(op.codes.index('con')), id])
                    continue
                if re.match(op.variable_usage, lexem) != 'None' and op.operators.count(lexem) == 0:
                    id = identifier_id(identifier_hash, lexem)
                    identifier_hash.append([id, lexem, 'var'])
                    lexem_hash.append([row_number, lexem, str(op.codes.index('id')), id])
        if delimiter:
            lexem_hash.append([row_number, ';', str(op.codes.index(';')), ' '])
    sa.syntax_analyzer(program, lexem_hash, identifier_hash, const_hash)
    xls_write(lexem_hash, identifier_hash, const_hash)


def xls_write(lexem_hash,identifier_hash,const_hash):
    with open('csv\\lexems.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(array_lexems)
        writer.writerows(lexem_hash)
    with open('csv\\identifiers.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(array_identifiers)
        writer.writerows(identifier_hash)
    with open('csv\\consts.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(array_consts)
        writer.writerows(const_hash)
    #merge_all_to_a_book(glob.glob("csv\\lexems.csv"), "xls\\lexems.xlsx")
    #merge_all_to_a_book(glob.glob("csv\\identifiers.csv"), "xls\\identifiers.xlsx")
    #merge_all_to_a_book(glob.glob("csv\\consts.csv"), "xls\\consts.xlsx")


def identifier_id(hash, lexem):
    iterator = 0
    identificator = 0
    for i in hash:
        current_hash = hash[iterator]
        if current_hash.count(lexem) != 0:
            return hash.index(i)
        else:
            identificator = len(hash)
        iterator = iterator + 1
    return identificator


def merge_codes():
    codes_list = ' |,'
    for i in op.codes:
        codes_list = codes_list + i + ' |,'
    return codes_list


def line_counter(file):
    return len((file.read()).split('\n'))


def check_for_prohibits(lexem):
    for i in op.prohibited:
        if lexem.find(i) is not -1:
            return False


def check_if_delimiter_presented(row):
    if row.find('if') != -1:
        return row
    if row.find('iterate') != -1:
        return row
    if row.find('finish') != -1:
        return row
    if row.find('else') != -1:
        return row
    if row.find(';') != -1 and row[len(row)-1] is ';':
        row = row.strip(';')
        return row
    else:
        return False
