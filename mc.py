import re
from tkinter import END, Button, Entry, Label, Text, Tk
from typing import List, Self


class Validator:

    def __init__(self):
        super().__init__()
        
        self.grammar = {
            "Sen": ["De", "As", "Ex", "Ec", "Lf"],
            "De": ['V', "Id", ":", "TD"],
            "As": ["Id", "=", "Ex"],
            'V': ["var"],
            "TD": ["int", "float", "string"],
            "Ex": ["T", "Ex+T", "Ex-T"],
            "T": ["Fa", "T*Fa", "T/Fa"],
            "Fa": ["Id", "En", "PiExPf", "Dec", "Ca"],
            "Pi": ["("],
            "Pf": [")"],
            "Id": ["L", "(L|D)*"],
            "L": ["[a-zA-Z]"], 
            "En": ["D+", "Dec"],
            "Dec": ["D+.+D+"],
            "D": ["[0-9]"],
            "Ec": ["if Pi Eb Pf B else B", "while Pi Eb Pf B", "print Pi Ca Pf"],
            "Eb": ["Ex", "Cl", "Ex"],
            "Cl": ["<", ">", "<=", ">=", "==", "!=", "="],
            "B": ["Ci", "Sen*", "Cf"],
            "Ci": ["{"],
            "Cf": ["}"],
            "Lf": ["Id", "Pi", "Ar", "Pf"],
            "Ar": ["Ex", "Ar,Ex"],
            "Ca": ['"Car+"\"'],
            "Car": ["L", "D", "Ce"],
            "Ce": ["."]
        }

    def validate(self, code: str) -> bool:
        if code == "":
            raise ValueError("No code provided. Please enter some code to validate.")

        if not self._validate_parentheses(code):
            return False

        if not self._validate_brackets(code):
            return False

        if not self._validate_braces(code):
            return False

        if not self._validate_quotes(code):
            return False

        if not self._validate_symbols(code):
            return False

        if not self._validate_grammar(code):
            return False

        print("Input válido!")
        return True

    def _validate_parentheses(self, code: str) -> bool:
        if code.count("(") != code.count(")"):
            raise ValueError("Error de paréntesis")
        return True

    def _validate_brackets(self, code: str) -> bool:
        if code.count("[") != code.count("]"):
            raise ValueError("Error de corchetes")
        return True

    def _validate_braces(self, code: str) -> bool:
        if code.count("{") != code.count("}"):
            raise ValueError("Error de llaves")
        return True

    def _validate_quotes(self, code: str) -> bool:
        if code.count("\"") % 2 != 0:
            raise ValueError("Error de comillas")

        if code.count("'") % 2 != 0:
            raise ValueError("Error de comillas")
        return True

    def _validate_symbols(self, code: str) -> bool:
        SYMBOL_PATTERN = r"([\{\}\(\)\[\],:+\-*/=<>!\s])"
        tokens = re.split(SYMBOL_PATTERN, code, maxsplit=1)
        symbol_stack = []

        for t in tokens:
            if t in self.grammar:
                if t not in self.grammar[symbol_stack[-1]]:
                    return False
                symbol_stack.pop()
            else:
                symbol_stack.append(t)

            if t in ["(", "[", "{"]:
                symbol_stack.append(t)

            elif t in [")", "]", "}"]:
                if len(symbol_stack) == 0 or symbol_stack[-1] == "V":
                    raise ValueError("Error de paréntesis")
                symbol_stack.pop()

            elif symbol_stack and symbol_stack[-1] in self.grammar:
                if t not in self.grammar[symbol_stack[-1]]:
                    raise ValueError("Error de sintaxis")
                symbol_stack.pop()

            else:
                raise ValueError("Error desconocido")

        if len(symbol_stack) > 0:
            raise ValueError("Faltan cerrar paréntesis o falta terminar producción")
        return True

    def _validate_grammar(self, code: str) -> bool:
        tokens = re.split(r"([\{\}\(\)\[\],:+\-*/=<>!\s])", code, maxsplit=1)
        symbol_stack = ["V"]

        for t in tokens:
            if t in self.grammar:
                if t not in self.grammar[symbol_stack[-1]]:
                    return False
                symbol_stack.pop()
            else:
                symbol_stack.append(t)

        if len(symbol_stack) > 1:
            return False
        return True


# GUI setup
root = Tk()
root.title("Code Validator")
text = Text(root)
text.focus()
text.__format__= str.format
text.pack()

# Add labels
errors_label = Label(root, text="Errors:")
errors_label.pack()
errors_label.config(text="")

# Add buttons
validator = Validator()
Button(root, text="Clear", command=lambda: text.event_delete("0.0", END) and errors_label.clipboard_clear()).pack()
Button(root, text="Check", command=lambda: errors_label.config(text="Input sin errores" if validator.validate(text.get("1.0", END))==True else "Errors found")).pack()
# Run the GUI
root.mainloop()