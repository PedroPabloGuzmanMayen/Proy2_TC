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
def find_epsilon_productions(grammar):
    epsilon_productions = set()
    # Para cada produccion se verifica si alguna es vacia
    for lhs, rules in grammar.productions.items():
        for rhs in rules:
            if not rhs:
                epsilon_productions.add(lhs)
    return epsilon_productions

def delete_epsilon_productions(grammar):
    epsilon_productions = find_epsilon_productions(grammar)

    if not epsilon_productions:
        return

    new_productions = {}

    for lhs, rules in grammar.productions.items():
        new_productions[lhs] = []
        for rhs in rules:
            new_productions[lhs].append(rhs)

            if lhs in epsilon_productions:
                new_rhs = rhs.copy()
                if new_rhs:
                    new_rhs.remove(lhs)
                    if new_rhs:
                        new_productions[lhs].append(new_rhs)
    grammar.productions = new_productions

def find_non_binarized_expressions(grammar):
    non_binarized = []

    for lhs, rules in grammar.productions.items():
        for rhs in rules:
            if len(rhs) > 2:
                non_binarized.append((lhs,rhs))
    return non_binarized

def binarize_expression(grammar):
    non_binarized = find_non_binarized_expressions(grammar)

    for lhs, rhs in grammar.productions.items():
        while len(rhs) > 2:
            new_non_terminal = f"{lhs}_1"
            grammar.non_terminals.append(new_non_terminal)
            grammar.productions[new_non_terminal] = [rhs[1:]]
            rhs = [rhs[0], new_non_terminal]
        grammar.productions[lhs] = [rhs]

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
