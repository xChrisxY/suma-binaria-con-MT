import tkinter as tk
from tkinter import ttk
import re

# Configuración de la máquina de Turing: (estado, símbolo) -> (nuevo_estado, símbolo_escrito, dirección)
LEFT = -1
RIGHT = 1  
STAY = 0  
SUMA_BINARIA = 0

transitions = {
    
    ('q0', '1'): ('q1', '1', RIGHT),  
    ('q1', '0'): ('q2', '0', RIGHT),  
    
    
    ('q2', '1'): ('q3', '1', RIGHT),  
    ('q2', '0'): ('q3', '0', RIGHT),  
    ('q2', '+'): ('q5', '+', RIGHT), 
    
    
    ('q3', '1'): ('q3', '1', RIGHT), 
    ('q3', '0'): ('q3', '0', RIGHT),  
    ('q3', '+'): ('q5', '+', RIGHT), 
    ('q3', '='): ('q_accept', '=', STAY),  
    
    ('q5', '1'): ('q6', '1', RIGHT),  
    ('q6', '0'): ('q3', '0', RIGHT),  
    
    ('q0', '0'): ('q_reject', '0', STAY),  
    ('q1', '1'): ('q_reject', '1', STAY),  
    ('q3', ' '): ('q_reject', ' ', STAY),  
    ('q5', '='): ('q_reject', '=', STAY),  
}

def sumarBinarios(tape):

    binarios = []
    cadena = ""
    global SUMA_BINARIA
    
    for i in tape:

        if i != "+" and i != "=":
            cadena += i
        else:
            binarios.append(cadena)
            cadena = ""

    suma_decimal = sum(int(b,2) for b in binarios)
    
    SUMA_BINARIA = bin(suma_decimal)[2:]
    

def turing_machine(cadena):

    pattern = r"^10\+([01]+(\+[01]+)*)?=$"

    estado = "inicio"
    i = 0

    while i < len(cadena):
        simbolo = cadena[i]

        if estado == "inicio":
            # La cadena debe comenzar con "10"
            if bool(re.match(pattern, cadena)):
                i += 2
                estado = "numero_binario"
            else:
                return False

        elif estado == "numero_binario":
            # Nos encontramos en una parte de número binario (0 o 1)
            if simbolo in "01":
                i += 1
            elif simbolo == "+":
                i += 1
                estado = "operador"
            elif simbolo == "=":
                i += 1
                estado = "final"
            else:
                return False

        elif estado == "operador":
            # Después de un "+" debería haber otro número binario
            if simbolo in "01":
                i += 1
                estado = "numero_binario"
            else:
                return False

        elif estado == "final":
            # La máquina debería terminar en el estado final cuando ve el "="
            return i == len(cadena)

    sumarBinarios(cadena)
    
    return estado == "final"


def check_tapes():
   
    for tape in tapes:
        accepted = turing_machine(tape)


        row = len(result_frame.grid_slaves()) // 2 + 1  
        bg_color = "#A7F3D0" if accepted else "#FECACA"  

        tk.Label(result_frame, text=tape, font=('Arial', 10), bg=bg_color, width=25, relief="solid").grid(
            row=row, column=0, padx=5, pady=2)

        result_text = f'{SUMA_BINARIA}' if accepted else "RECHAZADA"
        tk.Label(result_frame, text=result_text, font=('Arial', 10), bg=bg_color, width=25, relief="solid").grid(
            row=row, column=1, padx=5, pady=2)

    tapes.clear()  

def add_entry():
    """Agrega una entrada a la lista de cadenas."""
    tape = entry_var.get()
    if tape:  
        tapes.append(tape)
        entry_var.set("")  

root = tk.Tk()
root.title("Simulación de Máquina de Turing - Patrón 'abb'")
root.geometry("600x600")
root.configure(bg="#1E293B")

tapes = []  
style = ttk.Style()
style.theme_use("clam")  # Usar tema moderno 'clam'
style.configure("TButton", font=("Arial", 12), padding=6)
style.configure("TEntry", font=("Arial", 12), padding=5)

title_label = tk.Label(root, text="Máquina de Turing", font=("Arial", 20, "bold"), bg="#1E293B", fg="#F1F5F9")
title_label.pack(pady=10)

title_label_2 = tk.Label(root, text="Se aceptan cadenas de binarios separados por el símbolo +", font=("Arial", 10, "bold"), bg="#1E293B", fg="#F1F5F9")
title_label_2.pack(pady=5)

title_label_3 = tk.Label(root, text="La cadena debe empezar por '10' y debe terminar con el símbolo '='", font=("Arial", 10, "bold"), bg="#1E293B", fg="#F1F5F9")
title_label_3.pack(pady=5)

entry_var = tk.StringVar()
entry_field = ttk.Entry(root, textvariable=entry_var, width=40)
entry_field.pack(pady=10)

button_frame = tk.Frame(root, bg="#1E293B")
button_frame.pack(pady=5)

add_button = ttk.Button(button_frame, text="Agregar Cadena", command=add_entry)
add_button.grid(row=0, column=0, padx=5)

check_button = ttk.Button(button_frame, text="Validar Cadenas", command=check_tapes)
check_button.grid(row=0, column=1, padx=5)

result_frame = tk.Frame(root, bg="#1E293B")
result_frame.pack(pady=20)

tk.Label(result_frame, text="Cadena", font=('Arial', 12, 'bold'), width=25, bg="#374151", fg="#F1F5F9", relief="solid").grid(
    row=0, column=0, padx=5, pady=5)
tk.Label(result_frame, text="Resultado", font=('Arial', 12, 'bold'), width=25, bg="#374151", fg="#F1F5F9", relief="solid").grid(
    row=0, column=1, padx=5, pady=5)

root.mainloop()

