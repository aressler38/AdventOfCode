
class Emulator:
    def __init__(self):
        self.rax = 0
        self.rbx = 0
        self.rcx = 0
        self.eip = 0
        self.jumped = False
        self.program = []
        self.output = []

    def run(self):
        try:
            while True:
                opcode, operand = self.program[self.eip:2 + self.eip]
                self.run_opcode(opcode, operand)
                if not self.jumped:
                    self.eip += 2
                self.jumped = False
        except ValueError as e:
            if str(e.args[0]).startswith("not enough values to unpack"):
                pass
            else:
                print(e)
        except Exception as error:
            print(error)

    def combo_operand(self, operand: int):
        if 0 < operand < 4:
            return operand
        elif operand == 4:
            return self.rax
        elif operand == 5:
            return self.rbx
        elif operand == 6:
            return self.rcx
        else:
            raise ValueError(f"{operand} is not a valid operand")

    def run_opcode(self, opcode: int, operand: int):
        if opcode == 0:
            return self.adv(operand)
        elif opcode == 1:
            return self.bxl(operand)
        elif opcode == 2:
            return self.bst(operand)
        elif opcode == 3:
            return self.jnz(operand)
        elif opcode == 4:
            return self.bxc(operand)
        elif opcode == 5:
            return self.out(operand)
        elif opcode == 6:
            return self.bdv(operand)
        elif opcode == 7:
            return self.cdv(operand)
        else:
            raise ValueError(f"{opcode} is not a valid opcode")

    def adv(self, operand: int):
        self.rax = self.rax // (2 ** self.combo_operand(operand))

    def bxl(self, operand: int):
        self.rbx ^= operand

    def bst(self, operand: int):
        self.rbx = self.combo_operand(operand) % 8

    def jnz(self, operand: int):
        if self.rax != 0:
            self.eip = operand
            self.jumped = True

    def bxc(self, operand: int):
        # ignore operand
        self.rbx ^= self.rcx

    def out(self, operand: int):
        combo_result = self.combo_operand(operand) % 8
        self.output.append(combo_result)

    def bdv(self, operand: int):
        self.rbx = self.rax // (2 ** self.combo_operand(operand))

    def cdv(self, operand: int):
        self.rcx = self.rax // (2 ** self.combo_operand(operand))

    def load_rom(self):
        with open("../../data/day17-input.txt") as f:
            parts = f.read().split('\n\n')
            assert len(parts) == 2
            registers = [int(value.split(':')[1].strip()) for value in parts[0].split('\n')]
            self.rax = registers[0]
            self.rbx = registers[1]
            self.rcx = registers[2]
            self.program.extend([int(n) for n in parts[1].split(':')[1].strip().split(',')])
        return self

    def reset(self):
        self.rax = 0
        self.rbx = 0
        self.rcx = 0
        self.eip = 0
        self.jumped = False
        self.output = []

