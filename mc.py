import code
import re    # import regular expression library
import tkinter    # import tkinter library

# Gramática modelada como diccionario
grammar = {
    "Mc": r"^Sen*$",
    "Sen": r"^(De|As|Ex|Ec|Lf)$",  
    "De": r"^var\s\w+\s*:\s*(int|float|string)$",
    "As": r"^\w+\s*=\s*Ex$",
    "V": r"^var$",
    "TD": r"^(int|float|string)$",
    "Ex": r"^(T|Ex(\+|-)T)$",
    "T": r"^(Fa|T(\*|\/)Fa)$", 
    "Fa": r"^\w+|\d+|(\()Ex(\))|\d+\.\d+|\"[^\"]*\"",
    "Ec": r"^(if|\w+while)\s*\([^\)]*\)\s*Ex\s*(<=|>=|==|!=)\s*Ex\s*{Sen*}",
    "Eb": r"^Ex\s*(<=|>=|==|!=)\s*Ex$",
    "B": r"^{Sen*}$",
    "Lf": r"^\w+\s*\([^\)]*\)$",
    "Ar": r"^Ex(,Ex)*$", 
    "Ca": r'^"[^"]*"'
}

# Función de validación
def validate(code):
    code = text.get("1.0", "end") 
    lines = code.split("\n")

    for i, line in enumerate(lines):
        token = line.split(" ")[0]
        if token in grammar:
            if not re.match(grammar[token], line): 
                error["text"] = "Error en línea " + str(i+1)
                return
            else:
                error["text"] = "Token inválido en línea " + str(i+1)  
                return
    
    error["text"] = "Código válido"

# Interfaz gráfica
root = tkinter.Tk()
text = tkinter.Text(root)
text.pack()

validate_button = tkinter.Button(root, text="Validar", command=lambda: validate(text.get("1.0", "end-1c")))

validate_button.pack()

error = tkinter.Label(root)
error.pack()

root.mainloop()