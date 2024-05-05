import tkinter as tk

class Interpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, code):
        result = ""
        for line in code.split(";"):
            line = line.strip()
            if line:
                try:
                    if line.startswith("int") or line.startswith("string"):
                        type_, rest = line.split(" ", 1)
                        var_name, value = map(str.strip, rest.split("="))
                        if type_ == "int":
                            self.variables[var_name] = int(value)
                        elif type_ == "string":
                            self.variables[var_name] = value.strip('"')
                    elif line.startswith("print(") and line.endswith(")"):
                        content = line[len("print("):-1]
                        if "+" in content:
                            parts = content.split("+")
                            result += "".join([str(eval(part.strip(), {}, self.variables)) for part in parts]) + "\n"
                        else:
                            result += str(eval(content, {}, self.variables)) + "\n"
                    else:
                        result += str(eval(line, {}, self.variables)) + "\n"
                except SyntaxError:
                    result += "Erro de sintaxe\n"
                except NameError:
                    result += "Erro: Variável não definida\n"
                except Exception as e:
                    result += f"Erro: {e}\n"
        return result.strip()

def run_code():
    try:
        code = code_entry.get("1.0", tk.END).strip()
        result = interpreter.interpret(code)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
    except Exception as e:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Erro: {e}\n")

interpreter = Interpreter()

# Criando a janela principal
root = tk.Tk()
root.title("Interpreter")

# Campo de entrada para o código
code_entry = tk.Text(root, height=10, width=40)
code_entry.pack()

# Botão "Run"
run_button = tk.Button(root, text="Run", command=run_code)
run_button.pack()

# Área de saída para o resultado
output_text = tk.Text(root, height=5, width=40)
output_text.pack()

root.mainloop()
