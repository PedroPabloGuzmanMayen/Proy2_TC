from src.CNF import convert_to_cnf
from src.Grammar import Grammar

# Define la gramática
terminals = ["cooks", "drinks", "eats", "cuts", "in", "with", "he", "she", "cat", "dog", "beer", "cake", "juice", "meat", "soup", "fork", "knife", "oven", "spoon", "a", "the"]
non_terminals = ["S", "VP", "PP", "NP", "V", "P", "N", "Det"]
initial_symbol = "S"
productions = {
    "S": [["NP", "VP"]],
    "VP": [["VP", "PP"], ["V", "NP"], ["cooks"], ["drinks"], ["eats"], ["cuts"]],
    "PP": [["P", "NP"]],
    "NP": [["Det", "N"], ["he"], ["she"]],
    "V": [["cooks"], ["drinks"], ["eats"], ["cuts"]],
    "P": [["in"], ["with"]],
    "N": [["cat"], ["dog"], ["beer"], ["cake"], ["juice"], ["meat"], ["soup"], ["fork"], ["knife"], ["oven"], ["spoon"]],
    "Det": [["a"], ["the"]]
}

# Crea la gramática y conviértela a CNF
grammar = Grammar(terminals, non_terminals, initial_symbol, productions)
convert_to_cnf(grammar)  # Convierte la gramática a CNF

# Pruebas de frases aceptadas y no aceptadas
phrases = [
    ("he eats a cake", True),  # Debería ser aceptada
    ("the dog drinks the juice", True),  # Debería ser aceptada
    ("she cake drinks", False),  # No debería ser aceptada
    ("cat a the", False)  # No debería ser aceptada
]

# Ejecuta el algoritmo CYK en cada frase
for phrase, expected in phrases:
    input_string = phrase.split()
    result, tree, exec_time = grammar.cyk_parse(input_string)
    print(f"Phrase: '{phrase}' - Expected: {'Accepted' if expected else 'Rejected'}, Result: {'Accepted' if result else 'Rejected'}")
    if result:
        print("Parse Tree:", tree)
    print(f"Execution Time: {exec_time:.6f} seconds\n")
