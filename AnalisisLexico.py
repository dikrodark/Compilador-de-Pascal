import re

class RiscVGenerator:
    def __init__(self):
        self.data_section = []
        self.text_section = ["main:"]
        self.variables = {}
        self.label_count = 0
        self.for_stack = []

    def unique_label(self, base):
        self.label_count += 1
        return f"{base}_{self.label_count}"

    def declare_variable(self, name, vartype):
        if vartype == "integer":
            self.data_section.append(f"{name}: .word 0")
            self.variables[name] = "int"
        elif vartype == "real":
            self.data_section.append(f"{name}: .float 0.0")
            self.variables[name] = "float"

    def generate(self, lines):
        for line in lines:
            line = line.strip()
            if line.startswith("DECLARE"):
                _, name, _, vartype = line.split()
                self.declare_variable(name, vartype)
            elif line.startswith("READ"):
                var = line.split()[1]
                if self.variables[var] == "int":
                    self.text_section += [
                        "li a7, 5",
                        "ecall",
                        f"sw a0, {var}"
                    ]
                else:
                    self.text_section += [
                        "li a7, 6",
                        "ecall",
                        f"s.s fa0, {var}"
                    ]
            elif line.startswith("PRINT"):
                content = line[6:].strip()
                if content.startswith('"'):
                    label = self.unique_label("msg")
                    self.data_section.append(f'{label}: .asciiz {content}')
                    self.text_section += [
                        f"la a0, {label}",
                        "li a7, 4",
                        "ecall"
                    ]
                elif content in self.variables:
                    vartype = self.variables[content]
                    if vartype == "int":
                        self.text_section += [
                            f"lw a0, {content}",
                            "li a7, 1",
                            "ecall"
                        ]
                    else:
                        self.text_section += [
                            f"l.s fa0, {content}",
                            "li a7, 2",
                            "ecall"
                        ]
                    # Optional: print newline
                    self.text_section += [
                        "li a0, 10",
                        "li a7, 11",
                        "ecall"
                    ]
            elif ":=" in line:
                target, expr = line.split(":=")
                target = target.strip()
                expr = expr.strip()
                tokens = expr.split()

                if len(tokens) == 1:
                    # Simple assignment
                    if self.variables[target] == "int":
                        if tokens[0].isdigit():
                            self.text_section += [
                                f"li t0, {tokens[0]}",
                                f"sw t0, {target}"
                            ]
                        else:
                            self.text_section += [
                                f"lw t0, {tokens[0]}",
                                f"sw t0, {target}"
                            ]
                    else:
                        # real (float) assignment
                        self.text_section += [
                            f"l.s f0, {tokens[0]}",
                            f"s.s f0, {target}"
                        ]
                elif len(tokens) == 3:
                    op1, operator, op2 = tokens
                    if self.variables[target] == "int":
                        self.text_section += [
                            f"lw t0, {op1}",
                            f"lw t1, {op2}",
                        ]
                        if operator == '+':
                            self.text_section.append("add t2, t0, t1")
                        elif operator == '-':
                            self.text_section.append("sub t2, t0, t1")
                        elif operator == '*':
                            self.text_section.append("mul t2, t0, t1")
                        elif operator == '/':
                            self.text_section.append("div t2, t0, t1")
                        self.text_section.append(f"sw t2, {target}")
                    else:
                        self.text_section += [
                            f"l.s f1, {op1}",
                            f"l.s f2, {op2}"
                        ]
                        if operator == '+':
                            self.text_section.append("fadd.s f3, f1, f2")
                        elif operator == '-':
                            self.text_section.append("fsub.s f3, f1, f2")
                        elif operator == '*':
                            self.text_section.append("fmul.s f3, f1, f2")
                        elif operator == '/':
                            self.text_section.append("fdiv.s f3, f1, f2")
                        self.text_section.append(f"s.s f3, {target}")
            elif line.startswith("FOR_INICIO"):
                match = re.match(r"FOR_INICIO (\w+) := (\d+) TO (\d+)", line)
                var, start, end = match.groups()
                start_label = self.unique_label("for_start")
                end_label = self.unique_label("for_end")
                self.for_stack.append((var, end, start_label, end_label))
                self.text_section += [
                    f"li t0, {start}",
                    f"sw t0, {var}",
                    f"{start_label}:",
                    f"lw t0, {var}",
                    f"li t1, {end}",
                    f"bgt t0, t1, {end_label}"
                ]
            elif line.startswith("FOR_FIN"):
                var, _, _, _ = self.for_stack[-1]
                start_label, end_label = self.for_stack[-1][2], self.for_stack[-1][3]
                self.text_section += [
                    f"lw t0, {var}",
                    "addi t0, t0, 1",
                    f"sw t0, {var}",
                    f"j {start_label}",
                    f"{end_label}:"
                ]
                self.for_stack.pop()

        # Exit syscall
        self.text_section += [
            "li a7, 10",
            "ecall"
        ]

    def emit(self):
        return (
            ".data\n" + "\n".join(self.data_section) +
            "\n\n.text\n.globl main\n" + "\n".join(self.text_section)
        )


# === EJEMPLO DE USO ===
code_lines = [
    "DECLARE i : integer",
    "FOR_INICIO i := 1 TO 5",
    "PRINT i",
    "FOR_FIN i"
]

gen = RiscVGenerator()
gen.generate(code_lines)
output = gen.emit()
print(output)
