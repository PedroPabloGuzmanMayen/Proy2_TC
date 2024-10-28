from Grammar import Grammar
import re

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
    grammar.non_terminals.insert(0, "S0")
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
    '''
                    if character in appearances:

                    appearances[terminal].append(rule)
                else:
                    appearances[terminal] = []
                    appearances[terminal].append(rule)
    '''
    non_binarized = {}

    for lhs, rules in grammar.productions.items():
        for rhs in rules:
            if len(rhs) > 2 :
                if lhs in non_binarized:
                    non_binarized[lhs].append(rhs)
                else:
                    non_binarized[lhs] = []
                    non_binarized[lhs].append(rhs)
    return non_binarized

def replace_terminals(grammar):
    record = {}
    #Crear nuevas producciones para cada terminal
    for terminal in grammar.terminals:
        record[terminal] = "X" + terminal
        grammar.productions["X" + terminal] = [[terminal]]

    for production in grammar.productions:
        for rule in grammar.productions[production] :
            if len(rule) > 1:
                intersect = set(rule).intersection(set(record))
                if len(intersect) != 0:
                    old_list = grammar.productions[production].pop(grammar.productions[production].index(rule))
                    value = intersect.pop()
                    new_list = list(map(lambda x: record[value] if x == value else x, old_list ))
                    grammar.productions[production].append(new_list)
    
'''
Esta funcion convierte producciones no binarizadas en producciones binarias
'''

def binarize_expression(grammar):
    replace_terminals(grammar)
    counter = 0
    is_binarized = False
    non_binarized_expressions = find_non_binarized_expressions(grammar) #Obtener las expresiones no binarizada
    while not is_binarized:
        for expression in non_binarized_expressions:
            for rule in non_binarized_expressions[expression]:
                new_prod = "S" + str(counter) #Definir el nombre de la nueva producción
                old_list = grammar.productions[expression].pop(grammar.productions[expression].index(rule)) #Guardar el valor de la lista antes de binarizar la expresión
                print("Old", old_list)
                new_values = old_list[1:]
                print("New values: ", new_values)
                grammar.productions[new_prod] = [new_values]
                new_list = [old_list[0], new_prod]
                print(new_list)
                grammar.productions[expression].append(new_list)
                counter += 1

        non_binarized_expressions = find_non_binarized_expressions(grammar)
        
        if (len(list(non_binarized_expressions))) == 0:
            is_binarized = True



'''
2. find_unit_productions y delete_unit_productions
Estas funciones buscan producciones unitarias y las eliminan, sustituyéndolas por producciones equivalentes.
'''
def find_unit_productions(grammar):
    unit_productions = {}
    for lhs, rules in grammar.productions.items():
        for rhs in rules:
            if len(rhs) == 1 and rhs[0] in grammar.non_terminals:
                if lhs in unit_productions:
                    unit_productions[lhs].append(rhs)
                else:
                    unit_productions[lhs] = []
                    unit_productions[lhs].append(rhs)
    return unit_productions

'''
Elimina las producciones unitarias
'''
def delete_unit_productions(grammar):
    unit_productions = find_unit_productions(grammar)
    print("initial unit prods", unit_productions)
    is_unit = False #Verifica si hay nuevas transiciones unitarias
    while not is_unit:
        for prod, rule in unit_productions.items():
            for production in rule:
                old_value = grammar.productions[prod].pop(grammar.productions[prod].index(production)) #Eliminar la producción unitaria
                print("Old vale: ", old_value)
                new_values = grammar.productions[prod]
                grammar.productions[prod] = grammar.productions[prod] + grammar.productions[old_value[0]] #Añadir las nuevas transiciones

        unit_productions = find_unit_productions(grammar) #Verificar si hay más transiciones unitarias

        if len(unit_productions) == 0:
            is_unit = True
'''
'''



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
    "S": [["NP", "VP", "P", "N", "PP", "V"], ["ε"]],
    "VP": [["VP", "PP"], ["V", "NP"], ["cooks"], ["drinks"], ["eats"], ["cuts"], ["cuts", "VP"]],
    "PP": [["P", "NP"], ["Det"]],
    "NP": [["Det", "N"], ["he"], ["she"]],
    "V": [["cooks", "drinks"], ["drinks"], ["eats"], ["cuts"]],
    "P": [["in"], ["with"]],
    "N": [["cat"], ["dog"], ["beer"], ["cake"], ["juice"], ["meat"], ["soup"], ["fork"], ["knife"], ["oven"], ["spoon"]],
    "Det": [["a"], ["the"], ["VP"]]
}

grammar = Grammar(terminals, non_terminals, initial_symbol, productions)


delete_epsilon_productions(grammar)



print(find_unit_productions(grammar))

binarize_expression(grammar)

delete_unit_productions(grammar)

for i, j in grammar.productions.items():
    print(i, j)

