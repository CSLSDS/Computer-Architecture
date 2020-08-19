"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.op_size = 1
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010

    def load(self, program):
        """Load a program into memory."""
        address = 0
        with open(sys.argv[1]) as f:
            for line in f:
                line = line.split('#')
                num = line[0].strip()
                if num != '':
                    instruct_base2 = int(num, 2)
                    self.ram[address] = instruct_base2
                    address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            cmd = self.ram_read(self.pc)
            print(bin(cmd))
            if cmd == self.LDI:
                regix = self.ram[self.pc + 1]
                print(f'regix: {regix}')
                num2reg = self.ram[self.pc + 2]
                print(f'num2reg: {num2reg}')
                self.reg[regix] = num2reg
                print(f'self.reg[{regix}] = {num2reg}')
                self.op_size = cmd >> 6

            elif cmd == self.PRN:
                regix = self.ram[self.pc + 1]
                print('prn')
                print(self.reg[regix])
                self.op_size = cmd >> 6

            elif cmd == self.MUL:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]

                self.alu('MUL', reg_a, reg_b)
                print('mul')

                self.op_size = cmd >> 6

            elif cmd == self.HLT:
                running = False
                self.op_size = cmd >> 6
                print('halt')
            print(f'incrementing self.pc ({self.pc}) by self.op_size+1 ({self.op_size + 1})')
            self.pc += (self.op_size + 1)
            print(f'self.pc: {self.pc}')