import customtkinter as ctk
from .color_theme import get_palette
from src.Grammar import Grammar
from src.CNF import convert_to_cnf  # Asegúrate de importar la función de conversión
import time

class GrammarApp(ctk.CTk):
    def __init__(self, grammar):
        super().__init__()

        self.geometry("800x600")
        self.title("Grammar and Lambda Calculator")
        
        self.update_theme()

        self.left_frame = ctk.CTkFrame(self, width=300, corner_radius=10, fg_color=self.colors["base"])
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

        self.right_frame = ctk.CTkFrame(self, width=500, corner_radius=10, fg_color=self.colors["surface1"])
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

        self.theme_button = ctk.CTkButton(self.left_frame, text="Cambiar Tema", command=self.toggle_theme,
                                          fg_color=self.colors["overlay1"], text_color=self.colors["text"])
        self.theme_button.grid(row=0, column=0, padx=10, pady=10, sticky="ne")

        self.label = ctk.CTkLabel(self.left_frame, text="Gramática", text_color=self.colors["text"])
        self.label.grid(row=1, column=0, padx=10, pady=10)

        self.cnf_button = ctk.CTkButton(self.left_frame, text="Convertir a CNF", command=self.convert_to_cnf,
                                        fg_color=self.colors["sapphire"], text_color=self.colors["text"])
        self.cnf_button.grid(row=2, column=0, padx=10, pady=10)

        self.input_label = ctk.CTkLabel(self.left_frame, text="Cadena para analizar:", text_color=self.colors["text"])
        self.input_label.grid(row=3, column=0, padx=10, pady=10)

        self.input_entry = ctk.CTkEntry(self.left_frame, width=250, fg_color=self.colors["surface0"], text_color=self.colors["text"])
        self.input_entry.grid(row=4, column=0, padx=10, pady=10)

        self.cyk_button = ctk.CTkButton(self.left_frame, text="Ejecutar CYK", command=self.run_cyk,
                                        fg_color=self.colors["lavender"], text_color=self.colors["text"])
        self.cyk_button.grid(row=5, column=0, padx=10, pady=10)

        self.output_label = ctk.CTkLabel(self.right_frame, text="Resultado:", text_color=self.colors["subtext0"])
        self.output_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.output_text = ctk.CTkTextbox(self.right_frame, width=450, height=200, fg_color=self.colors["surface0"],
                                          text_color=self.colors["text"])
        self.output_text.grid(row=1, column=0, padx=10, pady=10)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.left_frame.rowconfigure(0, weight=1)
        self.right_frame.columnconfigure(0, weight=1)

        self.grammar = grammar

    def update_theme(self):
        # Actualiza la paleta de colores
        self.colors = get_palette()
        self.configure(bg_color=self.colors["base"])
        self.update_idletasks()

    def toggle_theme(self):
        ctk.set_appearance_mode("Light" if ctk.get_appearance_mode() == "Dark" else "Dark")
        self.update_theme()

    def convert_to_cnf(self):
        convert_to_cnf(self.grammar)
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", f"Gramática convertida a CNF:\n{self.grammar.to_json()}")

    def run_cyk(self):
        input_string = self.input_entry.get().strip().split()
        if not input_string:
            self.output_text.insert("1.0", "Por favor, ingresa una cadena.")
            return

        accepted, parse_tree, exec_time = self.grammar.cyk_parse(input_string)
        
        self.output_text.delete("1.0", "end")
        result_msg = f"Cadena {'aceptada' if accepted else 'rechazada'}.\nTiempo de ejecución: {exec_time:.4f} segundos\n"
        if accepted:
            result_msg += f"Parse Tree: {parse_tree}\n"
        self.output_text.insert("1.0", result_msg)

