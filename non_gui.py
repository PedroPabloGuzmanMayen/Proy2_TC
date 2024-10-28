from src.CNF import convert_to_cnf
from src.Grammar import Grammar
import time

def run_cyk(grammar, input_string):
    """Ejecuta el análisis CYK sobre una cadena dada y muestra el resultado en la terminal."""
    input_string = input_string.strip().split()
    if not input_string:
        print("Por favor, ingresa una cadena válida.")
        return

    start_time = time.time()
    accepted, parse_tree, exec_time = grammar.cyk_parse(input_string)
    exec_time = time.time() - start_time

    result_msg = f"Cadena {'aceptada' if accepted else 'rechazada'}.\nTiempo de ejecución: {exec_time:.4f} segundos\n"
    if accepted:
        result_msg += f"Parse Tree: {parse_tree}\n"
    print(result_msg)

if __name__ == "__main__":
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

    grammar = Grammar(terminals, non_terminals, initial_symbol, productions)
    convert_to_cnf(grammar)

    print("Gramática convertida a CNF con éxito.")
    print("Introduce una cadena para analizar o 'salir' para terminar.")

    while True:
        input_string = input("Cadena: ")
        if input_string.lower() == "salir":
            print("Finalizando el programa.")
            break
        run_cyk(grammar, input_string)

