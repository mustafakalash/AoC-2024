from enum import Enum

class Opcode(Enum):
    ADV = 0b000
    BXL = 0b001
    BST = 0b010
    JNZ = 0b011
    BXC = 0b100
    OUT = 0b101
    BDV = 0b110
    CDV = 0b111

class Computer:
    def __init__(self, file):
        self.instr_ptr = 0
        self.outs = []
        
        with open(file) as f:
            def extract_value(line):
                return line.split(":")[1].strip()
            
            self.a = int(extract_value(f.readline()))
            self.b = int(extract_value(f.readline()))
            self.c = int(extract_value(f.readline()))
            f.readline()
            self.program = [int(op) for op in extract_value(f.readline()).split(",")]

    def run(self):
        try:
            while True:
                opcode = Opcode(self.program[self.instr_ptr])
                operand = self.program[self.instr_ptr + 1]

                if self.call(opcode, operand):
                    self.instr_ptr += 2
        except IndexError:
            return ",".join(map(str, self.outs))
        
    def reset(self):
        self.a = 0
        self.b = 0
        self.c = 0
        self.outs = []
        self.instr_ptr = 0
        
    def find_copy(self):
        a = 0
        while a < 8 ** len(self.program):
            self.reset()
            self.a = a
            self.run()
            
            if self.outs == self.program:
                return a
            
            if self.program[-len(self.outs):] == self.outs:
                a *= 8
            else:
                a += 1

    def cmb(self, operand):
        return [0, 1, 2, 3, self.a, self.b, self.c, None][operand]
    
    def divide(self, operand):
        return self.a // (2 ** self.cmb(operand))
    
    def mod8(self, operand):
        return self.cmb(operand) % 0b1000
    
    def call(self, opcode, operand):
        fnc = getattr(self, Opcode(opcode).name.lower())
        return fnc(operand)
    
    def adv(self, operand):
        self.a = self.divide(operand)

        return True

    def bxl(self, operand):
        self.b = self.b ^ operand

        return True

    def bst(self, operand):
        self.b = self.mod8(operand)

        return True

    def jnz(self, operand):
        if self.a == 0:
            return True
        
        self.instr_ptr = operand

        return False

    def bxc(self, _):
        self.b = self.b ^ self.c

        return True

    def out(self, operand):
        self.outs.append(self.mod8(operand))

        return True

    def bdv(self, operand):
        self.b = self.divide(operand)

        return True

    def cdv(self, operand):
        self.c = self.divide(operand)

        return True
    
computer = Computer("17/input")
print(computer.run(), computer.find_copy())