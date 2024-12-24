from enum import Enum
import re

class Wire:
    def __init__(self, name, value = None):
        self.name = name
        self.value = value

    def get_place_value(self):
        return int(self.name[1:])
    
    @staticmethod
    def get_wire_name(prefix, place_value):
        return f"{prefix}{place_value:02d}"

    def get_prefix(self):
        return self.name[0]

    def is_input(self):
        return self.get_prefix() in Device.INPUT_WIRES
    
    def is_output(self):
        return self.get_prefix() == Device.OUTPUT_WIRES

    def __eq__(self, other):
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)

class Operation(Enum):
    AND = "AND"
    OR = "OR"
    XOR = "XOR"

    def run(self):
        return {
            Operation.AND: lambda x, y: x & y,
            Operation.OR: lambda x, y: x | y,
            Operation.XOR: lambda x, y: x ^ y
        }[self]

class Instruction:
    def __init__(self, in1, in2, operation, output):
        self.in1 = in1
        self.in2 = in2
        self.operation = operation
        self.output = output

    def run(self):
        if self.in1.value is None or self.in2.value is None:
            return False
        
        self.output.value = self.operation.run()(self.in1.value, self.in2.value)
        return True
    
    def inputs(self):
        return self.in1, self.in2

class Device:
    OUTPUT_WIRES = "z"
    INPUT_WIRES = "x", "y"
    BAD_OUTPUTS = 8

    def __init__(self, file):
        self.wires = set()
        self.instructions = []
        self.ran = False
        with open(file) as f:
            line = f.readline().strip()
            while line:
                name, value = line.split(": ")
                self.wires.add(Wire(name, int(value)))
                line = f.readline().strip()
            
            for line in f:
                line = line.strip()
                if not line:
                    continue

                instruction, output = line.split(" -> ")

                pattern = f"({'|'.join([op.name for op in Operation])})"
                operation = Operation(re.search(pattern, instruction).group())
                in1, in2 = instruction.split(f" {operation.name} ")

                output, in1, in2 = self.get_wire(output), self.get_wire(in1), self.get_wire(in2)
                self.wires.update([output, in1, in2])
                self.instructions.append(Instruction(in1, in2, operation, output))

    def get_wire(self, name):
        for wire in self.wires:
            if wire.name == name:
                return wire
            
        return Wire(name)
    
    def get_wires_by_prefix(self, prefix):
        wires = filter(lambda wire: wire.get_prefix() == prefix, self.wires)
        return sorted(wires, key=lambda wire: wire.name)
    
    def get_number(self, prefix):
        number = 0
        for wire in self.get_wires_by_prefix(prefix):
            place_value = wire.get_place_value()
            number |= (wire.value << place_value)

        return number

    def reset(self):
        for wire in self.wires:
            if not wire.is_input():
                wire.value = None

    def find_instruction_by_output(self, output):
        for instruction in self.instructions:
            if instruction.output == output:
                return instruction
            
    def find_instructions_by_input(self, input):
        instructions = []
        for instruction in self.instructions:
            if input in instruction.inputs():
                instructions.append(instruction)
        return instructions

    def trace_wire(self, name):
        wire = self.get_wire(name)
        instruction = self.find_instruction_by_output(wire)

        instructions = [instruction]
        for wire in instruction.inputs():
            if not wire.is_input():
                instructions.extend(self.trace_wire(wire.name))

        return instructions
    
    def is_bad_output(self, instruction):
        # Output wires should be XOR unless it's the last bit
        if instruction.output.is_output() and instruction.output is not self.get_wires_by_prefix(Device.OUTPUT_WIRES)[-1]:
            if instruction.operation != Operation.XOR:
                return True
        # Intermediate gates should not be XOR
        elif not (instruction.output.is_output() or any(wire.is_input() for wire in instruction.inputs())):
            if instruction.operation == Operation.XOR:
                return True
        # Gates with inputs that are input wires should be XOR -> XOR or AND -> OR unless it's the first bit
        elif all(wire.is_input() and not wire.get_place_value() == 0 for wire in instruction.inputs()):
            expectedNextOp = Operation.XOR if instruction.operation is Operation.XOR else Operation.OR
            nextOps = list(instr.operation for instr in self.find_instructions_by_input(instruction.output))

            if not any(nextOp == expectedNextOp for nextOp in nextOps):
                return True
        
        return False

    def find_bad_outputs(self):
        if self.ran:
            output = self.get_number(Device.OUTPUT_WIRES)
        else:
            output = self.run()

        inputs = (self.get_number(prefix) for prefix in Device.INPUT_WIRES)
        expected = sum(inputs)

        place_value = 0
        bad_outputs = set()
        checked_instructions = set()
        while expected:
            if expected & 1 != output & 1:
                instructions = self.trace_wire(Wire.get_wire_name(Device.OUTPUT_WIRES, place_value))
                for instruction in instructions:
                    if instruction in checked_instructions:
                        continue
                    checked_instructions.add(instruction.output)

                    if self.is_bad_output(instruction):
                        bad_outputs.add(instruction.output)

            expected >>= 1
            output >>= 1
            place_value += 1

        # I wanted to be cool and effecient and only check bad bits, but sometimes bad outputs can result in good bits :(
        if len(bad_outputs) < Device.BAD_OUTPUTS:
            for instruction in self.instructions:
                if instruction in checked_instructions:
                    continue
                checked_instructions.add(instruction.output)

                if self.is_bad_output(instruction):
                    bad_outputs.add(instruction.output)
        
        return ",".join(sorted(wire.name for wire in bad_outputs))

    def run(self):
        self.ran = True
        instructions = self.instructions.copy()
        while instructions:
            instruction = instructions.pop(0)
            if not instruction.run():
                instructions.append(instruction)
        
        return self.get_number(Device.OUTPUT_WIRES)
    
device = Device("24/input")
print(device.run())
print(device.find_bad_outputs())