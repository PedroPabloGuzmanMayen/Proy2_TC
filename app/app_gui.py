import customtkinter as ctk
from .color_theme import get_palette
from src.CNF import convert_to_cnf  # Importa la función de conversión completa

class GrammarApp(ctk.CTk):
    def __init__(self, grammar):
        super().__init__()

        self.geometry("800x600")
        self.title("Grammar and Lambda Calculator")
        
        # Frames
        self.left_frame = ctk.CTkFrame(self, width=300, corner_radius=10)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

        self.right_frame = ctk.CTkFrame(self, width=500, corner_radius=10)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

        # Widgets
        self.theme_button = ctk.CTkButton(self.left_frame, text="Cambiar Tema", command=self.toggle_theme)
        self.theme_button.grid(row=0, column=0, padx=10, pady=10, sticky="ne")

        self.label = ctk.CTkLabel(self.left_frame, text="Gramática")
        self.label.grid(row=1, column=0, padx=10, pady=10)

        self.cnf_button = ctk.CTkButton(self.left_frame, text="Convertir a CNF", command=self.convert_to_cnf)
        self.cnf_button.grid(row=2, column=0, padx=10, pady=10)

        self.input_label = ctk.CTkLabel(self.left_frame, text="Cadena para analizar:")
        self.input_label.grid(row=3, column=0, padx=10, pady=10)

        self.input_entry = ctk.CTkEntry(self.left_frame, width=250)
        self.input_entry.grid(row=4, column=0, padx=10, pady=10)

        self.cyk_button = ctk.CTkButton(self.left_frame, text="Ejecutar CYK", command=self.run_cyk)
        self.cyk_button.grid(row=5, column=0, padx=10, pady=10)

        self.output_label = ctk.CTkLabel(self.right_frame, text="Resultado:")
        self.output_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.output_text = ctk.CTkTextbox(self.right_frame, width=450, height=500)
        self.output_text.grid(row=1, column=0, padx=10, pady=10)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.left_frame.rowconfigure(0, weight=1)
        self.right_frame.columnconfigure(0, weight=1)

        self.grammar = grammar

        self.update_theme()

    def update_theme(self):
        """Aplica los colores del tema seleccionado a los elementos de la GUI."""
        self.colors = get_palette()
        self.configure(bg_color=self.colors["base"])

        self.left_frame.configure(fg_color=self.colors["base"])
        self.right_frame.configure(fg_color=self.colors["surface1"])
        self.theme_button.configure(fg_color=self.colors["overlay1"], text_color=self.colors["crust"])
        self.label.configure(text_color=self.colors["text"])
        self.input_label.configure(text_color=self.colors["subtext1"])
        self.input_entry.configure(fg_color=self.colors["surface0"], text_color=self.colors["subtext1"])
        self.cnf_button.configure(fg_color=self.colors["sapphire"], text_color=self.colors["crust"])
        self.cyk_button.configure(fg_color=self.colors["lavender"], text_color=self.colors["crust"])
        self.output_label.configure(text_color=self.colors["subtext0"])
        self.output_text.configure(fg_color=self.colors["surface0"], text_color=self.colors["subtext1"])
        self.update_idletasks() 

    def toggle_theme(self):
        """Alterna entre temas claro y oscuro."""
        ctk.set_appearance_mode("Light" if ctk.get_appearance_mode() == "Dark" else "Dark")
        self.update_theme()

    def convert_to_cnf(self):
        """Convierte la gramática actual a CNF y muestra el resultado."""
        convert_to_cnf(self.grammar)
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", f"Gramática convertida a CNF:\n{self.grammar.to_json()}")

    def run_cyk(self):
        """Ejecuta el algoritmo CYK en la cadena proporcionada."""
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

