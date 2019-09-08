import re
import operators as op

variables = {}


def syntax_analyzer(program, lexem_hash, identifier_hash, const_hash):
    identifiers = []
    for i in range(0, len(lexem_hash) - 1):
        lexem = lexem_hash[i][1]
        if lexem == ';':
            continue
        if lexem == 'if':
            if logical_expression_exists(lexem_hash, i, identifier_hash):
                if seek_for_end_statement(lexem_hash, i):
                    i = find_next_row_start(lexem_hash, lexem_hash[i][0], i)
                    continue
                else:
                    print(f"Invalid if statement on row {lexem_hash[i][0]}")
                    return
            else:
                print(f"Invalid if statement on row {lexem_hash[i][0]}")
                return
        if lexem == 'end':
            if seek_for_if_statement(lexem_hash, i):
                continue
            else:
                print(f"Missing end statement on row {lexem_hash[i][0]}")
                return
        if lexem == 'else':
            if seek_for_else(lexem_hash, i):
                i = find_next_row_start(lexem_hash, lexem_hash[i][0], i)
                continue
            else:
                print(f"Invalid else statement on row {lexem_hash[i][0]}")
                return
        if lexem == 'var':
            if lexem_hash[i + 1][1] in identifiers:
                print(f"Repeatable variable declaration on row {lexem_hash[i][0]}")
            if var_validation(lexem_hash, i, identifier_hash):
                identifiers.append(lexem_hash[i + 1][1])
                i = find_next_row_start(lexem_hash, lexem_hash[i][0], i)
            else:
                print(f"Invalid assignment operation on row {lexem_hash[i][0]}")
                return
        if lexem == 'iterate':
            iterate_check = iterate_validation(i, lexem_hash)
            if iterate_check == 0:
                continue
            else:
                print(iterate_check)
                return
        if lexem.isdigit():
            continue
        if lexem in op.operators:
            continue
        if identifier_exists(lexem, identifier_hash):
            if not identifier_declared(i, lexem_hash):
                if identifiers.count(lexem) == 0:
                    print(f"Identifier {lexem} is not declared on row {lexem_hash[i][0]}")


def logical_expression_exists(lexem_hash, index, identifier_hash):
    try:
        first_operand = lexem_hash[index + 1][1]
        operator = lexem_hash[index + 2][1]
        second_operand = lexem_hash[index + 3][1]
    except IndexError:
        return False
    if second_operand == ';':
        return False
    if valid_logical_operand(first_operand, identifier_hash):
        if operator in op.logical_operators:
            if valid_logical_operand(second_operand, identifier_hash):
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def iterate_validation(index, lexem_hash):
    following_lexem = lexem_hash[index + 1][1]
    if not following_lexem.isdigit():
        if not identifier_declared(index + 1, lexem_hash):
            return f"Iterator on row {lexem_hash[index][0]} is not valid"
    if not lexem_hash[index + 2][1] == 'times':
        return f"Missing times keyword on row {lexem_hash[index][0]}"
    if not iteration_closing(lexem_hash, index):
        return f"Finish operator is not valid or missing"
    else:
        return 0


def valid_logical_operand(operand, identifier_hash):
    if operand.isdigit() or identifier_exists(operand, identifier_hash):
        return True
    else:
        return False


def seek_for_else(lexem_hash, row):
    if row == 0:
        return False
    ifs_counter = 0
    elses_counter = 0
    for i in range(row, -1, -1):
        if i < 0:
            break
        if lexem_hash[i][1] == 'if':
            ifs_counter = ifs_counter + 1
        if lexem_hash[i][1] == 'else':
            elses_counter = elses_counter + 1
    if elses_counter == ifs_counter:
        return True
    else:
        return False


def seek_for_iterate(lexem_hash, row):
    paired = False
    if row == 0:
        return False
    for i in range(row, - 1, - 1):
        if i < 0 :
            break
        if lexem_hash[i][1] == 'finish':
            paired = True
            return paired
    return paired


def iteration_closing(lexem_hash, row):
    if row == 0:
        return False
    iterates_counter = 0
    finish_counter = 0
    for i in range(row, len(lexem_hash) - 1):
        if i < 0:
            break
        if lexem_hash[i][1] == 'iterate':
            iterates_counter = iterates_counter + 1
        if lexem_hash[i][1] == 'finish':
            finish_counter = finish_counter + 1
    if iterates_counter == finish_counter:
        return True
    else:
        return False


def seek_for_end_statement(lexem_hash, row):
    paired = False
    for i in range(row + 1, len(lexem_hash)):
        if lexem_hash[i][1] == 'end' and lexem_hash[i + 1][1] == ';':
            paired = True
            return paired
    return paired


def seek_for_if_statement(lexem_hash, row):
    if row == 0:
        return False
    ifs_counter = 0
    ends_counter = 0
    for i in range(0, len(lexem_hash) - 1):
        if i < 0:
            break
        if lexem_hash[i][1] == 'if':
            ifs_counter = ifs_counter + 1
        if lexem_hash[i][1] == 'end':
            ends_counter = ends_counter + 1
    if ends_counter == ifs_counter:
        return True
    else:
        return False


def var_validation(lexem_hash, index, identifier_hash):
    name = lexem_hash[index + 1][1]
    assignment_operator = lexem_hash[index + 2][1]
    if identifier_exists(name, identifier_hash):
        if assignment_operator == '=':
            if assignment_valid(lexem_hash, index + 3, identifier_hash):
                return True
            else:
                return False
    else:
        return False


def identifier_declared(index, lexem_hash):
    operand = lexem_hash[index][1]
    for i in range(0, index):
        lexem = lexem_hash[i][1]
        if lexem == 'var':
            if lexem_hash[i + 1][1] == operand:
                return True
    return False


def assignment_valid(lexem_hash, index, identifier_hash):
    operand = lexem_hash[index][1]
    if operand.isdigit() and lexem_hash[index + 1][1] == ';':
            return True
    elif identifier_exists(operand, identifier_hash) and identifier_declared(index, lexem_hash) and lexem_hash[index + 1][1] == ';':
        return True
    else:
        return False


def identifier_exists(identifier, identifier_hash):
    exists = False
    for ident in identifier_hash:
        if ident[1] == identifier:
            exists = True
            return exists
    return exists


def find_next_row_start(lexem_hash, current_row, current_index):
    for i in range(current_index, len(lexem_hash)-1):
        if int(lexem_hash[i][0]) > int(current_row):
            return int(lexem_hash[i][0])


# def identifier_list_lookup(identifier_hash, identifier):
#     for i in range(0, len(identifier_hash) - 1):
#         current_id = identifier_hash[i][1]
#         if identifier == current_id:
#             return True
#     return False


