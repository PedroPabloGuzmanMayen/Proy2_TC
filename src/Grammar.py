import time  # Importar la biblioteca time para medir el tiempo

class Grammar:
    def __init__(self, terminals, non_terminals, initial_symbol, productions):
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.initial_symbol = initial_symbol
        self.productions = productions

    def to_json(self):
        grammar_dict = {
            "terminals": self.terminals,
            "non_terminals": self.non_terminals,
            "initial_symbol": self.initial_symbol,
            "productions": self.productions
        }
        return json.dumps(grammar_dict, indent=4)

    def from_json(self, json_string):
        """Create a Grammar object from a JSON string."""
        data = json.loads(json_string)
        return Grammar(
            data["terminals"],
            data["non_terminals"],
            data["initial_symbol"],
            data["productions"]
        )

    def cyk_parse(self, input_string):
        start_time = time.time()  # Inicia la medición de tiempo

        n = len(input_string)
        T = [[set() for _ in range(n)] for _ in range(n)]
        parse_tree = [[[] for _ in range(n)] for _ in range(n)]

        # Fase 1: Llenar la diagonal con los terminales
        for j in range(n):
            for lhs, rules in self.productions.items():
                for rhs in rules:
                    if len(rhs) == 1 and rhs[0] == input_string[j]:
                        T[j][j].add(lhs)
                        parse_tree[j][j].append((lhs, input_string[j]))  # Estructura del nodo terminal

        # Fase 2: Llenar el resto de la tabla con combinaciones de subcadenas
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                for k in range(i, j):
                    for lhs, rules in self.productions.items():
                        for rhs in rules:
                            if len(rhs) == 2 and rhs[0] in T[i][k] and rhs[1] in T[k + 1][j]:
                                T[i][j].add(lhs)
                                # Agregar el nodo con una estructura más organizada y clara
                                parse_tree[i][j].append((lhs, parse_tree[i][k], parse_tree[k + 1][j]))

        end_time = time.time()  # Finaliza la medición de tiempo
        execution_time = end_time - start_time  # Calcula el tiempo de ejecución

        # Devolver el resultado de aceptación, el parse tree estructurado, y el tiempo de ejecución
        return ('S' in T[0][n - 1], parse_tree[0][n - 1] if 'S' in T[0][n - 1] else None, execution_time)

    def is_valid(self):
        # Verificar si el símbolo inicial está en los no terminales
        is_initial_valid = True if self.initial_symbol in self.non_terminals else False

        # Verificar que las producciones sean válidas
        is_productions_valid = all(
            lhs in self.non_terminals and
            all(all(symbol in self.non_terminals + self.terminals for symbol in rhs) for rhs in rules)
            for lhs, rules in self.productions.items()
        )
        return is_initial_valid and is_productions_valid