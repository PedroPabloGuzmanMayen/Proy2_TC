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
    #Este método se encarga de verificar si la gramática ingresada es válida
    def is_valid(self):
        pass
