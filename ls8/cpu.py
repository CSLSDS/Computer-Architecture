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
        self.FL = 0
        self.IS = [0] * 8
        self.IM = [1] * 8
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
        # TODO SC CMP - JEQ - JNE - JMP
        self.CMP =  0b10100111
        self.JEQ =  0b01010101
        self.JNE =  0b01010110
        self.JMP =  0b01010100
        self.ADDI = 0b10000000
        self.AND =  0b10100000
        self.OR =   0b10101010
        self.XOR =  0b10101011
        self.NOT =  0b01101001
        self.SHL =  0b10101100
        self.SHR =  0b10101101
        self.MOD =  0b10100100
        self.INT =  0b01010010
        self.IRET = 0b00010011
        self.ST =   0b10000100
        self.PRA =  0b01001000

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

    def alu(self, op, x, y):
        """ALU operations."""
        x = self.reg[x]
        y = self.reg[y]
        if op == "ADD":
            x += y
        #elif op == "SUB": etc
        elif op == "SUB":
            x -= y
        elif op == 'MUL':
            x *= y
        elif op == 'CMP':
            if x == y:
                self.FL = 1
            elif x > y:
                self.FL = 2
            else:
                self.FL = 4
        elif op == "AND":
            x &= y
        elif op == "OR":
            x |= y
        elif op == "XOR":
            x ^= y
        elif op == "NOT":
            x = ~x
        elif op == "SHL":
            x <<= y
        elif op == "SHR":
            x >>= y
        elif op == "MOD":
            if y == 0:
                print('i\'m sorry dave; i\'m afraid i can\'t do that')
                sys.exit(1)
            else:
                x %= y
        # AND OR XOR NOT SHL SHR MOD
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
                x = self.ram[self.pc + 1]
                y = self.ram[self.pc + 2]

                self.alu('MUL', x, y)
                print(f'##LS8##\n##LS8## MUL # {bin(cmd)}')
                # TODO add appropriate lines for verbose output == len(operation)
                print(f'##LS8##     multiply : {x} * {y}')
                #self.op_size = cmd >> 6
                ## SETPC = False
            
            elif cmd == self.ADD:
                x = self.ram[self.pc + 1]
                y = self.ram[self.pc + 2]

                self.alu('ADD', x, y)
                print(f'##LS8##\n##LS8## ADD # {bin(cmd)}')
                # TODO add appropriate lines for verbose output == len(operation)
                print(f'##LS8##     add : {self.reg[x]} + {self.reg[y]}')
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

                
        # AND OR XOR NOT SHL SHR MOD
            elif cmd == self.AND:
                # and
                x = self.ram[self.pc + 1]
                y = self.ram[self.pc + 2]
                self.alu('AND', x, y)
                print(f'##LS8##\n##LS8## AND # {bin(cmd)}')
                # TODO add appropriate lines for verbose output == len(operation)
                print(f'##LS8##    AND  : {self.reg[x]} and {self.reg[y]}\n##LS8##')
                #self.op_size = cmd >> 6
                ## SETPC = FALSE

            elif cmd == self.OR:
                # OR
                x = self.ram[self.pc + 1]
                y = self.ram[self.pc + 2]
                self.alu('OR', x, y)
                print(f'##LS8##\n##LS8## OR # {bin(cmd)}')
                # TODO add appropriate lines for verbose output == len(operation)
                print(f'##LS8##     OR : {self.reg[x]} and {self.reg[y]}\n##LS8##')
                #self.op_size = cmd >> 6
                ## SETPC = FALSE
            elif cmd == self.XOR:
                # XOR
                x = self.ram[self.pc + 1]
                y = self.ram[self.pc + 2]
                self.alu('XOR', x, y)
                print(f'##LS8##\n##LS8## XOR # {bin(cmd)}')
                # TODO add appropriate lines for verbose output == len(operation)
                print(f'##LS8##     XOR : {self.reg[x]} and {self.reg[y]}\n##LS8##')
                #self.op_size = cmd >> 6
                ## SETPC = FALSE
            elif cmd == self.NOT:
                # NOT
                x = self.ram[self.pc + 1]
                y = self.ram[self.pc + 2]
                self.alu('NOT', x, y)
                print(f'##LS8##\n##LS8## NOT # {bin(cmd)}')
                # TODO add appropriate lines for verbose output == len(operation)
                print(f'##LS8##     NOT : {self.reg[x]} and {self.reg[y]}\n##LS8##')
                #self.op_size = cmd >> 6
                ## SETPC = FALSE
            elif cmd == self.SHL:
                # SHL
                x = self.ram[self.pc + 1]
                y = self.ram[self.pc + 2]
                self.alu('SHL', x, y)
                print(f'##LS8##\n##LS8## SHL # {bin(cmd)}')
                # TODO add appropriate lines for verbose output == len(operation)
                print(f'##LS8##     SHL : {self.reg[x]} and {self.reg[y]}\n##LS8##')
                #self.op_size = cmd >> 6
                ## SETPC = FALSE
            elif cmd == self.SHR:
                # SHR
                x = self.ram[self.pc + 1]
                y = self.ram[self.pc + 2]
                self.alu('SHR', x, y)
                print(f'##LS8##\n##LS8## SHR # {bin(cmd)}')
                # TODO add appropriate lines for verbose output == len(operation)
                print(f'##LS8##    SHR  : {self.reg[x]} and {self.reg[y]}\n##LS8##')
                #self.op_size = cmd >> 6
                ## SETPC = FALSE
            elif cmd == self.MOD:
                # MOD
                x = self.ram[self.pc + 1]
                y = self.ram[self.pc + 2]
                self.alu('MOD', x, y)
                print(f'##LS8##\n##LS8## MOD # {bin(cmd)}')
                # TODO add appropriate lines for verbose output == len(operation)
                print(f'##LS8##     MOD : {self.reg[x]} and {self.reg[y]}\n##LS8##')
                #self.op_size = cmd >> 6
                ## SETPC = FALSE

            elif cmd == self.CMP:
                # compare
                x = self.ram[self.pc + 1]
                y = self.ram[self.pc + 2]
                self.alu('CMP', x, y)
                print(f'##LS8##\n##LS8## CMP # {bin(cmd)}')
                # TODO add appropriate lines for verbose output == len(operation)
                print(f'##LS8##     compare : {self.reg[x]} and {self.reg[y]}\n##LS8##')
                #self.op_size = cmd >> 6
                ## SETPC = FALSE

            elif cmd == self.JMP:
                # jump
                print(f'##LS8##\n##LS8## JMP # {bin(cmd)}')
                print(f'##LS8##    jump {bin(self.ram[self.pc + 1])}')
                self.pc = self.reg[self.ram[self.pc + 1]]
                ## SETPC = TRUE

            elif cmd == self.JEQ:
                # jump if equal
                print(f'##LS8##\n##LS8## JEQ # {bin(cmd)}')
                if self.FL & 0b1: # if CMP and equal
                    print(f'##LS8##    jump to specified {bin(self.ram[self.pc+1])}\n##LS8##')
                    self.pc = self.reg[self.ram[self.pc+1]] # jump to given
                else:
                    print(f'##LS8##    else jump next {bin(self.ram[self.pc+2])}\n##LS8##')
                    self.pc += 2 # else skip forward/cont
                ## SETPC = TRUE

            elif cmd == self.JNE:
                # jump if not equal
                print(f'##LS8##\n##LS8## JNE # {bin(cmd)}')
                print(f'##LS8## self.FL flag = {bin(self.FL)}')
                if not self.FL & 0b1: # if CMP and not equal:
                    print(f'##LS8##    not eq; jump to {bin(self.ram[self.pc + 1])}\n##LS8##')
                    self.pc = self.reg[self.ram[self.pc+1]] # jump to given
                else:
                    print(f'##LS8##    else jump next {bin(self.ram[self.pc + 2])}\n##LS8##')
                    self.pc += 2 # else skip fw/continue
                ## SETPC = TRUE

            elif cmd == self.ADDI:
                # add immediate
                print(f'##LS8##\n##LS8## ADDI # {bin(cmd)}')
                print(f'##LS8## add immediate to reg[{self.pc+1}] = {self.ram[self.pc+1]} + {self.ram[self.pc+2]}\n##LS8##')
                self.reg[self.ram[self.pc+1]] += self.ram[self.pc+2]
                ## SETPC = FALSE

            elif cmd == self.INT:
                # interrupt, flag bit given in IS
                self.IS |= (1 << self.reg[self.pc + 1])

            elif cmd == self.IRET:
                # return from interrupt
                for regix in range(6, -1, -1): # pop R0-R6
                    self.reg[regix] = self.ram_read(self.SP)
                    self.SP += 1
                self.FL = self.ram_read(self.SP) # pop flag
                self.SP += 1
                self.pc = self.ram_read(self.SP) # pop progcount
                self.SP += 1
                self.IS = [0] * 8 # restore original flag

            elif cmd == self.ST:
                # store val in reg b in address in reg a
                print(f'##LS8##\n##LS8## ST # {bin(cmd)}')
                print(f'##LS8## store val in reg[{self.ram[self.pc+1]} = {self.ram[self.pc+2]}\n##LS8##')
                self.reg[self.ram[self.pc+1]] = self.reg[self.ram[self.pc+2]]
            
            elif cmd == self.PRA:
                # print reg given in ascii
                print(f'##LS8##\n##LS8## PRA # {bin(cmd)}')
                print(f'{self.reg[self.ram[self.pc+1]]}') #TODO fig out ascii mod

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
            print(f'##LS8######     registers {self.reg}')
            
