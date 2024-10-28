from Grammar import Grammar

'''
esta función se encarga de hallar apariciones de una variable en las producciones de la gramática
'''

def find_appearances(grammar, character):
    appearances = {}
    for terminal in grammar.productions:
        for rule in grammar.productions[terminal]:
            if character in rule:
                if character in appearances:

                    appearances[terminal].append(rule)
                else:
                    appearances[terminal] = []
                    appearances[terminal].append(rule)
    return appearances

'''
Esta función debe eliminar el simbolo inicial (solo si es necesario) en las producciones
'''
def eliminate_start_symbol(grammar):
    new_initial_symbol = "S0"
    grammar.productions[new_initial_symbol] = [[grammar.initial_symbol]]  # Agregar la producción S0 -> S
    grammar.initial_symbol = new_initial_symbol  # Cambiar el valor del símbolo inicial de la gramática. 


'''
Esta funcion buscara producciones que puedan derivar en la cadena vacia
'''
def find_epsilon_productions(grammar):
    epsilon_productions = {}
    for terminal in grammar.productions:
        for rule in grammar.productions[terminal]:
            if "ε" in rule and terminal != grammar.initial_symbol:
                epsilon_productions[terminal] = rule
    return epsilon_productions
'''
Esta funcion eliminara las producciones epsilon presentes en la gramática
'''
def delete_epsilon_productions(grammar):
    epsilon_productions = find_epsilon_productions(grammar)
    is_Empty = False #Esta condición nos ayudará a determinar si surgen nuevas producciones epsilon en la gramática

    while not is_Empty: 
        for i in epsilon_productions:
            print("Prod", i)
            print(grammar.productions[i])
            grammar.productions[i].remove(["ε"]) #Remover la producción epsilon
        for terminal in epsilon_productions:
            appearances = find_appearances(grammar, terminal) #Hallamos las producciones en donde aparecen los terminales con producciones epsilon
            print("Appearances: ", appearances) 
            for variable in appearances:
                for rule in appearances[variable]:
                    print("Rule", rule)
                    if len(rule) >= 2: #Si la regla encontrada tiene una longitud mayor o igual a 2, eliminar la variable y añadir esanueva regla
                        print("Rule: ", rule)
                        print(terminal)
                        new_rule = [symbol for symbol in rule if symbol != str(terminal)]
                        print("New rule: ", new_rule)
                        grammar.productions[variable].append(new_rule)
                    else: #Si la rella tiene longitud 1, guardar la producción epsilon
                        grammar.productions[variable].append(["ε"])

        epsilon_productions = find_epsilon_productions(grammar) #Evauamos si con los cambios realizados, ahora la gramática ya no tiene producciones epsilon
        print("NEW", epsilon_productions)
        if len(list(epsilon_productions)) == 0: #Si ya no hay producciones epsilon, terminar el ciclo
            is_Empty = True
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


terminals = ["cooks", "drinks", "eats", "cuts", "in", "with", "he", "she", "cat", "dog", "beer", "cake", "juice", "meat", "soup", "fork", "knife", "oven", "spoon", "a", "the"]
non_terminals = ["S", "VP", "PP", "NP", "V", "P", "N", "Det"]
initial_symbol = "S"
productions = {
    "S": [["NP", "VP"], ["ε"]],
    "VP": [["VP", "PP"], ["V", "NP"], ["cooks"], ["drinks"], ["eats"], ["cuts"]],
    "PP": [["P", "NP"], ["Det"]],
    "NP": [["Det", "N"], ["he"], ["she"]],
    "V": [["cooks"], ["drinks"], ["eats"], ["cuts"]],
    "P": [["in"], ["with"]],
    "N": [["cat"], ["dog"], ["beer"], ["cake"], ["juice"], ["meat"], ["soup"], ["fork"], ["knife"], ["oven"], ["spoon"]],
    "Det": [["a"], ["the"]]
}

grammar = Grammar(terminals, non_terminals, initial_symbol, productions)



delete_epsilon_productions(grammar)

for i in grammar.productions:
    print(grammar.productions[i])