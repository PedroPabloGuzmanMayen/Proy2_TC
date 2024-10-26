import json
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
    #Crea una nueva 
    def from_json(self, json_string):
        """Create a Grammar object from a JSON string."""
        data = json.loads(json_string)
        return Grammar(
            data["terminals"],
            data["non_terminals"],
            data["initial_symbol"],
            data["productions"]
        )
    # Metodo para determinar si una cadena puede ser generada por CFN
    def cyk_parse(self, input_string):
        n = len(input_string)
        T = [[set() for _ in range(n)] for _ in range(n)]

        # Llenar la diagonal con los terminales
        for j in range(n):
            for lhs, rules in self.productions.items():
                for rhs in rules:
                    if len(rhs) == 1 and rhs[0] == input_string[j]:
                        T[j][j].add(lhs)

        # Fase 2: Llenar el resto de la tabla con combinaciones de subcadenas
        for length in range(2, n + 1): 
            for i in range(n - length + 1): 
                j = i + length - 1 
                for k in range(i, j): 
                    for lhs, rules in self.productions.items():
                        for rhs in rules:
                            if len(rhs) == 2 and rhs[0] in T[i][k] and rhs[1] in T[k + 1][j]:
                                T[i][j].add(lhs)
        return 'S' in T[0][n - 1]
    #Este método se encarga de verificar si la gramática ingresada es válida
    def is_valid(self):
        pass
