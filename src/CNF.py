from Grammar import Grammar

'''
Esta función debe eliminar el simbolo inicial (solo si es necesario) en las producciones
'''
def eliminate_start_symbol(grammar):
    # Si el simbolo inicial no es un no-terminal, no hacemos nada
    if grammar.initial_symbol not in grammar.non_terminals:
        return
    new_initial_symbol = "S'"

    # Verificar que el nuevo simbolo no exista en los no-terminales
    while new_initial_symbol in grammar.non_terminals:
        new_initial_symbol += "'"
    
    # Se agrega la nueva produccion para el nuevo simbolo inicial
    grammar.productions[new_initial_symbol] == [[grammar.initial_symbol]]
    grammar.initial_symbol == new_initial_symbol
    
    # Si esta el simbolo inicial transferimos las reglas
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
'''
Esta funcion eliminara las producciones que pueden derivar en la cadena vacia
'''
def delete_epsilon_productions(grammar):
    epsilon_productions = find_epsilon_productions(grammar)

    if not epsilon_productions:
        return

    new_productions = {}

    for lhs, rules in grammar.productions.items():
        new_productions[lhs] = []
        for rhs in rules:
            new_productions[lhs].append(rhs)
            # Si el lado izq. puede derivar en epsilo agregamos nuevas producciones
            if lhs in epsilon_productions:
                new_rhs = rhs.copy()
                if new_rhs: # Si la produccion no esta vacia se remueve el simbolo que produce epsilon
                    new_rhs.remove(lhs)
                    if new_rhs:
                        new_productions[lhs].append(new_rhs) # Se agrega si no esta vacia
    grammar.productions = new_productions
'''
Esta funcion busca que producciones tienen mas de 2 simbolos en el lado der.
'''
def find_non_binarized_expressions(grammar):
    non_binarized = []

    for lhs, rules in grammar.productions.items():
        for rhs in rules:
            if len(rhs) > 2:
                non_binarized.append((lhs,rhs))
    return non_binarized
'''
Esta funcion convierte producciones no binarizadas en producciones binarias
'''
def binarize_expression(grammar):
    non_binarized = find_non_binarized_expressions(grammar)

    for lhs, rhs in grammar.productions.items():
        while len(rhs) > 2:
            new_non_terminal = f"{lhs}_1"  # Se genera un nuevo no-terminal y se agrega a la lista de no-terminales
            grammar.non_terminals.append(new_non_terminal)
            # Se hace una nueva produccion con los simbolos restantes y se reemplaza la produccion original
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
