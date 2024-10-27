from app.app_gui import *
from src.CNF import convert_to_cnf
from src.Grammar import *

if __name__ == "__main__":
    # Configuración de gramática
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

    app = GrammarApp(grammar)
    app.mainloop()
