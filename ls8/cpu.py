"""CPU functionality."""

import sys


SP = 7
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0 # bitct bit count ticks runtime lines prog counter
        self.reg = [0] * 8
        self.reg[SP] = 0xf4
        #self.op_size = 1
        self.LDI =  0b10000010
        self.PRN =  0b01000111
        self.HLT =  0b00000001
        self.MUL =  0b10100010
        self.PUSH = 0b01000101
        self.POP =  0b01000110
        self.CALL = 0b01010000
        self.RET =  0b00010001
        self.ADD =  0b10100000

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
            #print(f'##LS8## CMD = self.ram_read(self.pc) ({bin(cmd)})')

            if cmd == self.LDI:
                print(f'##LS8##\n##LS8## LDI # load immediate {bin(cmd)}')
                regix = self.ram[self.pc + 1]
                print(f'##LS8## {bin(self.ram[self.pc+1])}     regix = self.ram[self.pc + 1] ({regix})')
                num2reg = self.ram[self.pc + 2]
                print(f'##LS8## {bin(self.ram[self.pc+2])}     num2reg = self.ram[self.pc + 2] ({num2reg})\n##LS8##')
                self.reg[regix] = num2reg
                #print(f'##LS8##     self.reg[{regix}] = {num2reg}')
                #self.op_size = cmd >> 6

            elif cmd == self.PRN:
                regix = self.ram[self.pc + 1]
                print(f'##LS8##\n##LS8## PRN # {bin(cmd)}')
                print(f'##LS8## {bin(self.ram[self.pc + 1])}    print val at self.reg[{self.ram[self.pc + 1]}]\n##LS8##')
                print(self.reg[regix])
                #self.op_size = cmd >> 6
                ## SETPC = False

            elif cmd == self.MUL:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]

                self.alu('MUL', reg_a, reg_b)
                print(f'##LS8##\n##LS8## MUL # {bin(cmd)}')
                # TODO add appropriate lines for verbose output == len(operation)
                print(f'##LS8##     multiply : {reg_a} * {reg_b}')
                #self.op_size = cmd >> 6
                ## SETPC = False
            
            elif cmd == self.ADD:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]

                self.alu('ADD', reg_a, reg_b)
                print(f'##LS8##\n##LS8## ADD # {bin(cmd)}')
                # TODO add appropriate lines for verbose output == len(operation)
                print(f'##LS8##     add : {self.reg[reg_a]} + {self.reg[reg_b]}')
                #self.op_size = cmd >> 6
                ## SETPC = False

            elif cmd == self.PUSH:
                self.reg[SP] -= 1 # shift ram index signifying sp to new 'top'
                value = self.reg[self.ram_read(self.pc + 1)]
                self.ram_write(self.reg[SP], value)
                print(f'##LS8##\n##LS8## PUSH # {bin(cmd)}')
                print(f'##LS8##     {bin(value)} push {value} (to RAM index {self.reg[SP]})')
                #self.op_size = cmd >> 6
                ## SETPC = False

            elif cmd == self.POP:
                # stack pointer assigned to designated top of 'stack'
                value = self.ram_read(self.reg[SP])
                self.reg[self.ram_read(self.pc + 1)] = value
                # increment to reduce/shift stack by one
                self.reg[SP] += 1
                print(f'##LS8##\n##LS8## POP # {bin(cmd)}')
                print(f'##LS8##     {bin(self.ram_read(self.reg[SP]))} pop {value} into self.reg[{self.ram_read(self.pc + 1)}]')
                #self.op_size = cmd >> 6
                ## SETPC = False
            
            elif cmd == self.CALL: # 0b01010000 aka bin(50)
                # calls a subroutine(fn) at address stored in reg
                # 1. addr of instr AFTER call is pushed onto stack
                #   allows return to initial position in instructions after sub
                # post_subroutine = self.ram_read(self.pc + 2)
                self.reg[SP] -= 1
                self.ram_write(self.reg[SP], (self.pc + 2))
                # pc set to addr stored in given reg, jump to location, 
                #   execute 1st instr, continue as necessary
                self.pc = self.reg[self.ram_read(self.pc + 1)]
                print(f'##LS8##\n##LS8## CALL # {bin(cmd)}')
                print(f'##LS8##     line {self.pc}\n##LS8##')
                ## SETPC = TRUE

            elif cmd == self.RET: # 0b00010001 aka bin(11)
                # return from the subroutine
                # pop the val from top of the stack and 'store' in pc
                print(f'##LS8##\n##LS8## RET # {bin(cmd)}')
                print(f'##LS8##     to line {self.ram_read(self.reg[SP])}')
                # set pc to return address
                self.pc = self.ram_read(self.reg[SP])
                self.reg[SP] += 1
                ## SETPC = TRUE

            elif cmd == self.HLT:
                running = False
                #self.op_size = cmd >> 6
                print(f'##LS8##\n##LS8## HLT # {bin(cmd)}')
                print(f'##LS8##     halting!\n##LS8## END')
                ## SETPC = TRUE

            SETPC = cmd & 0b10000
            if not SETPC:
                #print(f'##LS8##\n##LS8###### incrementing program counter ({self.op_size + 1} lines/bytes/cmds)')
                self.pc += (cmd >> 6) + 1
            else:
                continue
            #self.pc += (self.op_size + 1)
            print(f'##LS8######     program counter {self.pc}')
            print(f'##LS8######     TOP of RAM {[item for item in self.ram[0xf0:0xf6]]}')
            print(f'##LS8######     val at SP {self.ram_read(self.reg[SP])}')
