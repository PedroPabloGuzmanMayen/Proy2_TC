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
    new_productions = grammar.productions.copy()  # Copia de las producciones para iterar sin problemas

    for lhs, rules in new_productions.items():
        updated_rules = []  # Lista temporal para las reglas modificadas de `lhs`
        for rhs in rules:
            while len(rhs) > 2:
                new_non_terminal = f"{lhs}_1"  # Genera un nuevo no-terminal
                grammar.non_terminals.append(new_non_terminal)
                
                # Crea una nueva producción y reemplaza la producción original
                grammar.productions[new_non_terminal] = [rhs[1:]]
                rhs = [rhs[0], new_non_terminal]
                
            updated_rules.append(rhs)  # Añade la regla binarizada
        grammar.productions[lhs] = updated_rules  # Actualiza `grammar.productions` con las reglas modificadas


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
    while unit_productions:
        lhs, rhs = unit_productions.pop()
        # Remplazar la producción unitaria con producciones del RHS
        for production in grammar.productions[rhs]:
            if production not in grammar.productions[lhs]:
                grammar.productions[lhs].append(production)
        # Actualizar lista de producciones unitarias
        unit_productions = find_unit_productions(grammar)

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
