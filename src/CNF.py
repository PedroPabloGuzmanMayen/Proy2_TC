from src.Grammar import Grammar

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
    grammar.productions[new_initial_symbol] = [[grammar.initial_symbol]]  # Corrección aquí
    grammar.initial_symbol = new_initial_symbol  # Corrección en la asignación
        # Si el símbolo inicial original tenía producciones, transfiérelas al nuevo símbolo inicial
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
            # Solo agrega nuevas producciones si `lhs` produce ε
            if lhs in epsilon_productions and lhs in rhs:
                new_rhs = [s for s in rhs if s != lhs]
                if new_rhs and new_rhs not in new_productions[lhs]:
                    new_productions[lhs].append(new_rhs)
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

    for lhs, rhs in non_binarized:
        new_rhs = rhs[:]
        while len(new_rhs) > 2:
            new_non_terminal = f"{lhs}_{len(grammar.non_terminals)}"  # Evita nombres repetidos
            grammar.non_terminals.append(new_non_terminal)
            grammar.productions[new_non_terminal] = [new_rhs[1:]]
            new_rhs = [new_rhs[0], new_non_terminal]
        grammar.productions[lhs].append(new_rhs)

'''
1. find_null_productions y delete_null_productions
Estas funciones encuentran y eliminan producciones que derivan en la cadena vacía (ε), lo cual es necesario para la conversión a CNF.
'''
def find_null_productions(grammar):
    epsilon_productions = set()
    for lhs, rules in grammar.productions.items():
        for rhs in rules:
            if not rhs:  # Si la producción es una cadena vacía
                epsilon_productions.add(lhs)
    return epsilon_productions

def delete_null_productions(grammar):
    epsilon_productions = find_null_productions(grammar)
    if not epsilon_productions:
        return

    new_productions = {}
    for lhs, rules in grammar.productions.items():
        new_productions[lhs] = []
        for rhs in rules:
            if rhs:  # No es una producción vacía
                new_productions[lhs].append(rhs)
                for symbol in epsilon_productions:
                    if symbol in rhs:
                        # Crear una nueva producción sin el símbolo que produce ε
                        new_rhs = [s for s in rhs if s != symbol]
                        if new_rhs:
                            new_productions[lhs].append(new_rhs)
    grammar.productions = new_productions

'''
2. find_unit_productions y delete_unit_productions
Estas funciones buscan producciones unitarias y las eliminan, sustituyéndolas por producciones equivalentes.
'''
def find_unit_productions(grammar):
    unit_productions = []
    for lhs, rules in grammar.productions.items():
        for rhs in rules:
            if len(rhs) == 1 and rhs[0] in grammar.non_terminals:
                unit_productions.append((lhs, rhs[0]))
    return unit_productions

def delete_unit_productions(grammar):
    unit_productions = find_unit_productions(grammar)
    processed_units = set()
    while unit_productions:
        lhs, rhs = unit_productions.pop()
        if (lhs, rhs) in processed_units:
            continue  # Evita procesar las mismas producciones unitarias
        processed_units.add((lhs, rhs))

        for production in grammar.productions[rhs]:
            if production not in grammar.productions[lhs]:
                grammar.productions[lhs].append(production)
                # Solo agregamos la producción unitaria si es nueva
                if len(production) == 1 and production[0] in grammar.non_terminals:
                    unit_productions.append((lhs, production[0]))

'''
3. convert_to_cnf
Esta función aplica todos los pasos necesarios para convertir la gramática a CNF, llamando a las funciones anteriores y asegurando que todas las producciones cumplen con CNF.
'''

def convert_to_cnf(grammar):
    # 1. Eliminar producciones vacías
    delete_epsilon_productions(grammar)
    
    # 2. Eliminar producciones unitarias
    delete_unit_productions(grammar)
    
    # 3. Binarizar producciones
    binarize_expression(grammar)
    
    # 4. Asegurarse de que el símbolo inicial esté correctamente configurado
    eliminate_start_symbol(grammar)
