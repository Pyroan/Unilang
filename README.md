# Omnilang / Unilang (both working titles)

## THE BRIEF
This is an esoteric programming language where every unicode character corresponds to a unique operation or sequence of operations.

Okay so basically the way this works is it's a stack-based language
with a number of base operations. Unicode codepoints greater than that number go through sequences of the base ops.

For example, if `a` corresponds to the `sum` operation, and `b` corresponds to the `diff` operation, `c` might correspond to the program `ab`. If the numbers *`m`*, *`n`*, and *`o`* are on the stack, the programs may work like this

| Opcode | Program | Result |
| ------ | ------- | ------ |
| a      | a       |  m + n |
| b      | b       | m - n  |
| c      | aa      | (m + n) + o |

Following some kinda pseudo-binary counting system we could keep going

| Opcode | Program | Result |
| ------ | ------  | ------ |
| d      | ab      | (m + n) - o |
| e      | ba      | (m - n) + o |
| f      | bb      | (m - n) - o |

Todo: figure out some crap with arity if necessary. The stack might make it not matter

On the interpreter side... ideally we can reconstruct the program string from the codepoint of the character. the problem is that not all unicode codepoints are being used. We could try to create a subset of unicode but that's no fun and doesn't fit the brief anyway. We could also just _ignore_ them and escape them.

And sure it would be nice if codepoints made _sense_ but that would make this a lot harder so. Really part of this project is writing something that compiles to this.

## BASE OPS

### Integer Literals
- **num** - Push the given digit onto the stack. Crap that means 0 and f are equivalent and so are 1 and t

### Math
- **sum** - Pop the top two items off the stack, add them, and push the result
- **diff** - Pop the top two items off the stack, subtract the second from the first, and push the result
- **mult** - Pop the top two items off the stack, multiply them, and push the result.
- **div** - Pop the top two items off the stack, divide the first by the second (integer division), and push the result.
- **mod** - Pop the top two items off the stack, divide the first by the second, and return the remainder.
- **exp** - Pop the top two items off the stack, raise the first to the power of the second, and push the result

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
- ~~**true** - Push 1 onto the stack~~
- ~~**fals** - Push 0 onto the stack~~
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



| Character | Codepoint | Op   | Pops  |
| --------- | --------- | ---- | ----- |
| a | 97  | sum  | 2 |
| b | 98  | diff | 2 |
| c | 99  | copy | 1 |
| d | 100 | div  | 2 |
| e | 101 | exp  | 2 |
| f | 102 | flsh | X |
| g | 103 | gt   | 2 |
| h | 104 | hmm  | 0 |
| i | 105 | cin  | 0 |
| j | 106 | jt   | 2 |
| k | 107 | kill | 0 |
| l | 108 | lt   | 2 |
| m | 109 | mod  | 2 |
| n | 110 | nin  | 0 |
| o | 111 | cout | 1 |
| p | 112 | mult | 2 |
| q | 113 | eq   | 2 |
| r | 114 | roll | 1 | 
| s | 115 | swap | 0 |
| t | 116 | this | 0 |
| u | 117 | updt | 2 |
| v | 118 | nout | 1 |
| w | 119 | not  | 1 |
| x | 120 | exec | 1 |
| y | 121 | yeet | 1 |
| z | 122 | size | 0 |
| -- |-- |-- |-- |
| 0-9 | | num | 0 |

## Useful Non-base Ops