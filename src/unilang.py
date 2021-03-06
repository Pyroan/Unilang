import argparse
import sys
from opcodes import *
from compression import compress_program, decompress_program

# Execution Modes
EXECUTE = 0
STRINGL = 1
COMMENT = 2

class Unilang:
    tape = []
    stack = []
    ip = 0
    mode = EXECUTE

    def __init__(self, prog: str):
        self.tape = list(decompress_program(prog))

    def run(self, debug=False):
        if debug:
            print(''.join(self.tape))
        while self.ip < len(self.tape):
            if debug:
                print("Stack: " + ', '.join(map(str, self.stack)))
                print("ip: " + str(self.ip) + ', ins: ' + self.tape[self.ip] )
                input()


            if self.mode == EXECUTE:
                if self.tape[self.ip] in '0123456789':
                    self.stack.append(int(self.tape[self.ip]))
                elif self.tape[self.ip] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    self.stack.append(ord(self.tape[self.ip]) - ord('A') + 10)
                elif self.tape[self.ip] == SUM:
                    self.add()
                elif self.tape[self.ip] == DIFF:
                    self.diff()
                elif self.tape[self.ip] == COPY:
                    self.copy()
                elif self.tape[self.ip] == DIV:
                    self.div()
                elif self.tape[self.ip] == EXP:
                    self.exp()
                elif self.tape[self.ip] == FLSH:
                    self.flush()
                elif self.tape[self.ip] == GT:
                    self.gt()
                elif self.tape[self.ip] == HMM:
                    self.hmm()
                elif self.tape[self.ip] == CIN:
                    self.cin()
                elif self.tape[self.ip] == JT:
                    self.jt()
                elif self.tape[self.ip] == LT:
                    self.lt()
                elif self.tape[self.ip] == MOD:
                    self.mod()
                elif self.tape[self.ip] == NIN:
                    self.nin()
                elif self.tape[self.ip] == COUT:
                    self.cout()
                elif self.tape[self.ip] == MULT:
                    self.mult()
                elif self.tape[self.ip] == EQ:
                    self.eq()
                elif self.tape[self.ip] == ROLL:
                    self.roll()
                elif self.tape[self.ip] == SWAP:
                    self.swap()
                elif self.tape[self.ip] == THIS:
                    self.this()
                elif self.tape[self.ip] == UPDT:
                    self.updt()
                elif self.tape[self.ip] == NOUT:
                    self.nout()
                elif self.tape[self.ip] == NOT:
                    self.inv()
                elif self.tape[self.ip] == EXEC:
                    self.exec()
                elif self.tape[self.ip] == YEET:
                    self.yeet()
                elif self.tape[self.ip] == SIZE:
                    self.size()
                elif self.tape[self.ip] == TRUE:
                    self.true()
                elif self.tape[self.ip] == FALS:
                    self.fals()
                elif self.tape[self.ip] == LSHF:
                    self.lshf()
                elif self.tape[self.ip] == RSHF:
                    self.rshf()


                elif self.tape[self.ip] == CMNT:
                    self.mode = COMMENT
                elif self.tape[self.ip] == STR:
                    self.mode = STRINGL

                elif self.tape[self.ip] == KILL:
                    break
                
                else:
                    raise ValueError(
                        '{} is not a valid operation!'.format(self.tape[self.ip])
                    )
            
            elif self.mode == STRINGL:
                if self.tape[self.ip] == STR:
                    self.mode = EXECUTE
                else:
                    self.stack.append(ord(self.tape[self.ip]))

            elif self.mode == COMMENT:
                if self.tape[self.ip] == CMNT:
                    self.mode = EXECUTE
            
            self.ip += 1

    ############
    # BASE OPS #
    ############

    def pop(self):
        if len(self.stack) == 0:
            return 0
        else:
            return self.stack.pop()
    # Helper function to pop two items
    def pop2(self):
        a = self.pop()
        b = self.pop()
        return a, b

    # Math
    def add(self):
        a, b = self.pop2()
        self.stack.append(a+b)
    
    def diff(self):
        a, b = self.pop2()
        self.stack.append(b-a)
    
    def mult(self):
        a, b = self.pop2()
        self.stack.append(a*b)
    
    def div(self):
        a, b = self.pop2()
        self.stack.append(b//a)
    
    def mod(self):
        a, b = self.pop2()
        self.stack.append(b%a)
    
    def exp(self):
        a, b = self.pop2()
        self.stack.append(b**a)
    
    def lshf(self):
        a, b = self.pop2()
        self.stack.append(b<<a)
    
    def rshf(self):
        a, b = self.pop2()
        self.stack.append(b>>a)
    
    # I/O 
    def cin(self):
        s = input()
        for c in reversed(s):
            self.stack.append(ord(c))
    
    def nin(self):
        self.stack.append(int(input()))
    
    def cout(self):
        print(chr(self.pop()), end='')

    def nout(self):
        print(self.pop())
    
    # Comparison / Flow Control
    def eq(self):
        a, b = self.pop2()
        if a == b:
            self.stack.append(1)
        else:
            self.stack.append(0)
    
    def gt(self):
        a, b = self.pop2()
        if b > a:
            self.stack.append(1)
        else:
            self.stack.append(0)
    
    def lt(self):
        a, b = self.pop2()
        if b < a:
            self.stack.append(1)
        else:
            self.stack.append(0)
    
    def jt(self):
        a, b = self.pop2()
        if a > 0:
            self.ip = b - 1
    
    # logical NOT
    def inv(self):
        a = self.pop()
        if a == 0:
            self.stack.append(1)
        else:
            self.stack.append(0)
    
    def this(self):
        self.stack.append(self.ip)
    
    def flush(self):
        s = ''
        while len(self.stack) > 0:
            s += chr(self.pop())
        print(s)

    def exec(self):
        print("Oh no i'm not touching this one yet you can try again later.")

    def updt(self):
        a, b = self.pop2()
        self.tape[a] = chr(b)

    def hmm(self):
        pass

    def true(self):
        self.stack.push(1)
    
    def fals(self):
        self.stack.push(0)

    # Stack manipulation
    def swap(self):
        a, b = self.pop2()
        self.stack.append(a)
        self.stack.append(b)

    def roll(self):
        a = self.pop()
        self.stack = self.stack[a:] + self.stack[:a]

    def size(self):
        self.stack.append(len(self.stack))
    
    def copy(self):
        self.stack.append(self.stack[-1])

    def yeet(self):
        self.pop()
    

def main():
    parser = argparse.ArgumentParser(description="Unilang Interpreter")
    parser.add_argument('-p', '--prog', type=str,
        help='Execute a script given in the command line')
    parser.add_argument('-f', '--file', type=str, default='',
        help='Optionally specify the source file')
    parser.add_argument('-d', '--debug', action='store_true',
        help='Run in debug mode')
    parser.add_argument('-c', '--compress', action='store_true',
        help='Compress the given program instead of executing it.')
    parser.add_argument('--decompress', action='store_true')
    parser.add_argument('-o', '--outfile', type=str, default='',
        help='Optional file to output to')
    args = parser.parse_args()
    
    prog = ''
    if len(args.file) > 0:
        with open(args.file, 'r', encoding='utf-8') as f:
            prog = f.read()
    else:
        prog = args.prog
    
    if len(args.outfile) > 0:
        sys.stdout = open(args.outfile, 'w+', encoding='utf-8')

    if args.compress:
        print(compress_program(prog), end='')
    elif args.decompress:
        print(decompress_program(prog), end='')
    else:
        uni = Unilang(prog)
        uni.run(args.debug)


if __name__ == '__main__':
    main()
