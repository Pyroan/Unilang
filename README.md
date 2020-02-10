# Omnilang / Unilang (both working titles)

## BASIC USAGE
```
# Run program from command line
python src/unilang.py -p 'insert_program_here'

# Run program from file
python src/unilang.py -f name_of_file.uni

# Compress program
python src/unilang.py -cf name_of_file.uni

# Output to a file
python src/unilang.py -f input_file.uni -o output_file.uni

# Try "python src/unilang.py -h" for more options
```

## THE BRIEF
This is an esoteric programming language where every unicode character corresponds to a unique operation or sequence of operations.

Okay so basically the way this works is it's a stack-based language
with a number of base operations. Unicode codepoints greater than that number go through sequences of the base ops.

For example, if `a` corresponds to the `sum` operation, and `b` corresponds to the `diff` operation, `c` might correspond to the program `ab`. If the numbers *`m`*, *`n`*, and *`o`* are on the stack, the programs may work like this

| Opcode | Program | Result      |
| ------ | ------- | ----------- |
| a      | a       | m + n       |
| b      | b       | m - n       |
| c      | aa      | (m + n) + o |

Following some kinda pseudo-binary counting system we could keep going

| Opcode | Program | Result      |
| ------ | ------  | ------      |
| d      | ab      | (m + n) - o |
| e      | ba      | (m - n) + o |
| f      | bb      | (m - n) - o |

Todo: figure out some crap with arity if necessary. The stack might make it not matter

On the interpreter side... ideally we can reconstruct the program string from the codepoint of the character. the problem is that not all unicode codepoints are being used. We could try to create a subset of unicode but that's no fun and doesn't fit the brief anyway. We could also just _ignore_ them and escape them.

And sure it would be nice if codepoints made _sense_ but that would make this a lot harder so. Really part of this project is writing something that compiles to this.

## BASE OPS

### Math
- **sum** - Pop the top two items off the stack, add them, and push the result
- **diff** - Pop the top two items off the stack, subtract the second from the first, and push the result
- **mult** - Pop the top two items off the stack, multiply them, and push the result.
- **div** - Pop the top two items off the stack, divide the first by the second (integer division), and push the result.
- **mod** - Pop the top two items off the stack, divide the first by the second, and return the remainder.
- **exp** - Pop the top two items off the stack, raise the first to the power of the second, and push the result
- **lshf** - Pop the top two items, _a_ and _b_, off the stack, shift _b_ left by _a_ bits, and push the result onto the stack.
- **rshf** - Pop the top two items, _a_ and _b_, off the stack, shift _b_ right by _a_ bits, and push the result onto the stack.

### I/O
- **cin** - Push every character in an input string (in reverse order - first character in the input should be on the top of the stack)
- **nin** - Push input onto the stack as a base-10 number
- **cout** - Pop and output the top value of the stack as a Unicode character
- **nout** - Pop and output the top value of the stack as a base-10 number.

### Comparison/Flow Control
- **eq** - Pop the top two values of the stack. If both values are equal, push 1 onto the stack. Else, push 0.
- **gt** - Pop the top two values of the stack. If the first is greater than the second, push 1. Else, push 0.
- **lt** - Pop the top two values off the stack. If the first is less than the second, push 1. Else, push 0.
- **jt** - Jump if True: Pop the top two values off the stack. If the first is greater than 0, move the instruction pointer to the index given by the second value.
- **not** - Logical NOT: pop the top value of the stack. If it's 0, push 1. If it's nonzero, push 0
- **true** - Push 1 onto the stack
- **fals** - Push 0 onto the stack
- **exec** - Pop the top value off the stack, and run it as though it's a part of the program.
- **kill** - Close the program.
- **updt** - Pop two values, _n_ and _m_, off the stack. Replace the character at index _n_ in the program with codepoint _m_
- **hmm** - No Op

### Stack Manipulation
- **swap** - Swap the top two values of the stack
- **roll** - Pop the top value _n_ off the stack. Put top _n_ values of  the stack on the bottom of the stack, in order. i.e. if the stack is [1, 2, 3, 4, 5], and you roll 3, the stack will look like [3, 4, 5, 1, 2]
- **size** - Push the length of the stack onto the stack.
- **copy** - Push the top value of the stack onto the stack
- **yeet** - Pop the top value of the stack and discard it.
- **flsh** - Flush: Pop the entire stack and output it as a string
- **this** - Push the index of this instruction onto the stack (or, push the instruction pointer's current index onto the stack)

### Misc.
- **str** - Switch to/from string mode, pushing each character in the program onto the stack until you reach another str instruction
- **cmnt** - Switch to/from comment mode, every character up to the next cmnt instruction will be treated as a no-op



| Character | Codepoint | Op   | Pops  |
| --------- | --------- | ---- | ----- |
| `         | U+0060    | str  | 0     |
| a         | U+0061    | sum  | 2     |
| b         | U+0062    | diff | 2     |
| c         | U+0063    | copy | 1     |
| d         | U+0064    | div  | 2     |
| e         | U+0065    | exp  | 2     |
| f         | U+0066    | fals | 0     |
| g         | U+0067    | gt   | 2     |
| h         | U+0068    | hmm  | 0     |
| i         | U+0069    | cin  | 0     |
| j         | U+006A    | jt   | 2     |
| k         | U+006B    | kill | 0     |
| l         | U+006C    | lt   | 2     |
| m         | U+006D    | mod  | 2     |
| n         | U+006E    | nin  | 0     |
| o         | U+006F    | cout | 1     |
| p         | U+0070    | mult | 2     |
| q         | U+0071    | eq   | 2     |
| r         | U+0072    | roll | 1     |
| s         | U+0073    | swap | 0     |
| t         | U+0074    | true | 0     |
| u         | U+0075    | updt | 2     |
| v         | U+0076    | nout | 1     |
| w         | U+0077    | not  | 1     |
| x         | U+0078    | exec | 1     |
| y         | U+0079    | yeet | 1     |
| z         | U+007A    | size | 0     |
| {         | U+007B    | lshf | 2     |
| \|        | U+007C    | this | 0     |
| }         | U+007D    | rshf | 2     |
| ~         | U+007E    | cmnt | 0     |
| ␡         | U+007F    | flsh | X     |

## Useful Non-base Ops

| Character | Codepoint | Base Ops | Description |
| --------- | --------- | -------- | ----------- |
| ʷ         | U+02b7    | qw       | Not Equals  |