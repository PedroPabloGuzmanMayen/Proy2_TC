from src.Grammar import Grammar
from src.CNF import convert_to_cnf

def get_user_input():
    # Obtener terminales
    terminals = input("Ingrese los terminales, separados por comas (ej: a,b,c): ").strip().split(',')

    # Obtener no terminales
    non_terminals = input("Ingrese los no terminales, separados por comas (ej: S,A,B): ").strip().split(',')

    # Obtener símbolo inicial
    initial_symbol = input("Ingrese el símbolo inicial (ej: S): ").strip()

    # Obtener producciones
    productions = {}
    print("Ingrese las producciones. Use '->' para indicar la producción y '|' para separar alternativas.")
    print("Formato: S -> A B | a")
    print("Para finalizar, presione Enter sin ingresar nada.")
    while True:
        production_input = input("Producción: ").strip()
        if not production_input:
            break
        try:
            lhs, rhs = production_input.split("->")
            lhs = lhs.strip()
            rhs = [r.strip().split() for r in rhs.split("|")]
            productions[lhs] = rhs
        except ValueError:
            print("Formato incorrecto. Intente de nuevo.")

    return terminals, non_terminals, initial_symbol, productions

def main():
    # Solicitar datos de la gramática al usuario
    terminals, non_terminals, initial_symbol, productions = get_user_input()

    # Crear la gramática y convertirla a CNF
    grammar = Grammar(terminals, non_terminals, initial_symbol, productions)
    convert_to_cnf(grammar)

    # Mostrar la gramática en CNF
    print("\nGramática en Forma Normal de Chomsky (CNF):")
    print(grammar.to_json())

    # Solicitar cadena para análisis CYK
    input_string = input("\nIngrese la cadena a analizar (separada por espacios, ej: a b c): ").strip().split()

    # Ejecutar el algoritmo CYK y mostrar resultados
    accepted, parse_tree, exec_time = grammar.cyk_parse(input_string)
    print(f"\nResultado del análisis CYK para la cadena '{' '.join(input_string)}':")
    print("Cadena aceptada." if accepted else "Cadena rechazada.")
    print(f"Tiempo de ejecución: {exec_time:.6f} segundos")
    if accepted:
        print("Parse Tree:", parse_tree)

main()
