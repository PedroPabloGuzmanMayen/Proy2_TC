from Grammar import Grammar

'''
Esta función debe eliminar el simbolo inicial (solo si es necesario) en las producciones
'''
def eliminate_start_symbol(grammar):
    if grammar.initial_symbol not in grammar.non_terminals:
        return
    new_initial_symbol = "S'"

    while new_initial_symbol in grammar.non_terminals:
        new_initial_symbol += "'"

    grammar.productions[new_initial_symbol] == [[grammar.initial_symbol]]
    grammar.initial_symbol == new_initial_symbol
    
    if grammar.initial_symbol in grammar.productions:
        grammar.productions[new_initial_symbol].extend(grammar.productions[grammar.initial_symbol])

    del grammar.productions[grammar.initial_symbol]
'''
Esta funcion buscara producciones que puedan derivar en la cadena vacia
'''
def find_epsilon_productions():
    pass

def delete_epsilon_productions():
    pass

def find_non_binarized_expressions():
    pass
def binarize_expression():
    pass

def find_null_productions():
    pass

def delete_null_productions():
    pass

def find_unit_productions():
    pass

def delete_unit_productions():
    pass


def convert_to_cnf():
    pass
