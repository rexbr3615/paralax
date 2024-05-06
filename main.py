import tkinter as tk
from tkinter import filedialog
import random

class Interpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, code):
        result = ""
        code_lines = code.split("\n")  # Dividir o código por linhas
        i = 0
        while i < len(code_lines):
            line = code_lines[i].strip()
            if line:
                try:
                    if line.startswith("int") or line.startswith("string") or line.startswith("bool"):
                        type_, rest = line.split(" ", 1)
                        var_name, value = map(str.strip, rest.split("="))
                        if type_ == "int":
                            self.variables[var_name] = int(value)
                        elif type_ == "string":
                            self.variables[var_name] = value.strip('"')
                        elif type_ == "bool":
                            self.variables[var_name] = True if value.strip().lower() == "true" else False
                    elif line.startswith("print(") and line.endswith(")"):
                        content = line[len("print("):-1]
                        if "random_number" in content:
                            start = content.find("random_number(")
                            end = content.find(")", start)
                            args = content[start+len("random_number("):end].split(",")
                            min_value = int(args[0].strip())
                            max_value = int(args[1].strip())
                            value = random.randint(min_value, max_value)
                            result += content[:start] + str(value) + content[end+1:] + "\n"
                        else:
                            if "+" in content:
                                parts = content.split("+")
                                result += "".join([str(eval(part.strip(), {}, self.variables)) for part in parts]) + "\n"
                            else:
                                result += str(eval(content, {}, self.variables)) + "\n"
                    elif line.startswith("timer(") and line.endswith(")"):
                        params = line[len("timer("):-1].split(",")
                        time_unit = params[0].strip()
                        duration = int(params[1].strip())
                        if time_unit == "segundos":
                            root.after(duration * 1000, run_code)
                        elif time_unit == "milisegundos":
                            root.after(duration, run_code)
                    elif line.startswith("random_number(") and line.endswith(")"):
                        params = line[len("random_number("):-1].split(",")
                        min_value = int(params[0].strip())
                        max_value = int(params[1].strip())
                        result += str(random.randint(min_value, max_value)) + "\n"
                    elif line.startswith("if "):
                        condition = line[3:].strip()
                        if self.variables.get(condition, False):
                            # Encontra o bloco de código do 'if'
                            block = ""
                            while True:
                                i += 1
                                if i >= len(code_lines) or code_lines[i].strip() == "else:":
                                    break
                                block += code_lines[i] + "\n"
                            result += self.interpret(block)
                            if i < len(code_lines) and code_lines[i].strip() == "else:":
                                while True:
                                    i += 1
                                    if i >= len(code_lines) or code_lines[i].strip() == "endif":
                                        break
                    elif line.startswith("else:"):
                        # Encontra o bloco de código do 'else'
                        block = ""
                        while True:
                            i += 1
                            if i >= len(code_lines) or code_lines[i].strip() == "endif":
                                break
                            block += code_lines[i] + "\n"
                        result += self.interpret(block)
                    else:
                        result += str(eval(line, {}, self.variables)) + "\n"
                except SyntaxError:
                    result += "Erro de sintaxe\n"
                except NameError:
                    result += "Erro: Variável não definida\n"
                except Exception as e:
                    result += f"Erro: {e}\n"
            i += 1
        return result.strip()

def run_code():
    try:
        code = code_entry.get("1.0", tk.END).strip()
        result = interpreter.interpret(code)
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
        output_text.config(state=tk.DISABLED)
    except Exception as e:
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Erro: {e}\n")
        output_text.config(state=tk.DISABLED)

def new_file():
    code_entry.delete("1.0", tk.END)
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            code_entry.delete("1.0", tk.END)
            code_entry.insert("1.0", file.read())

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(code_entry.get("1.0", tk.END))

def save_file_as():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(code_entry.get("1.0", tk.END))

interpreter = Interpreter()

# Criando a janela principal
root = tk.Tk()
root.title("IDE")
root.iconbitmap("Paralax.ico")

# Criação da barra de menu
menubar = tk.Menu(root)

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Novo", command=new_file)
file_menu.add_command(label="Abrir", command=open_file)
file_menu.add_command(label="Salvar", command=save_file)
file_menu.add_command(label="Salvar como", command=save_file_as)
file_menu.add_separator()
file_menu.add_command(label="Sair", command=root.quit)
menubar.add_cascade(label="Arquivo", menu=file_menu)

edit_menu = tk.Menu(menubar, tearoff=0)
edit_menu.add_command(label="Desfazer")
edit_menu.add_command(label="Refazer")
edit_menu.add_separator()
edit_menu.add_command(label="Recortar")
edit_menu.add_command(label="Copiar")
edit_menu.add_command(label="Colar")
edit_menu.add_separator()
edit_menu.add_command(label="Selecionar tudo")
menubar.add_cascade(label="Editar", menu=edit_menu)

view_menu = tk.Menu(menubar, tearoff=0)
view_menu.add_command(label="Ampliar")
view_menu.add_command(label="Reduzir")
view_menu.add_command(label="Restaurar padrão")
menubar.add_cascade(label="Visualizar", menu=view_menu)

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="Sobre")
menubar.add_cascade(label="Ajuda", menu=help_menu)

root.config(menu=menubar)

# Campo de entrada para o código
code_entry = tk.Text(root, height=20, width=60)
code_entry.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Botão "Run"
run_button = tk.Button(root, text="Run", command=run_code)
run_button.pack(pady=5)

# Área de saída para o resultado
output_text = tk.Text(root, height=10, width=60)
output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Desabilitando a edição da área de saída
output_text.config(state=tk.DISABLED)

root.mainloop()
