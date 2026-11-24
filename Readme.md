# Nand2Tetris Capstone – Make the Computer Draw a Box

## Project Overview
This project focuses on building the Hack computer using HDL, developing a two-pass assembler in Python, and implementing a keyboard-controlled box using Hack Assembly Language.

## Project Structure

```text
Nand2Tetris_Capstone/
│
├── Part_A_Computer/
│   └── HDL files (CPU, Memory, Computer and supporting chips)
│
├── Part_B_Assembler/
│   ├── assembler.py
│   └── Test programs
│
├── Part_C_Box/
│   ├── Box.asm
│   └── Box.hack
│
└── Screenshots/
    ├── Part A/
    ├── Part B/
    └── Part C/
```

## Part A – Computer Construction
Implemented the CPU, Memory, and Computer chips using HDL.

**Tests performed:**
- CPU.tst
- Memory.tst
- ComputerAdd.tst
- ComputerMax.tst
- ComputerRect.tst

All tests passed successfully.

## Part B – Python Assembler
Developed a two-pass assembler that translates Hack Assembly instructions into 16-bit binary machine code.

**Features:**
- Label and symbol handling
- Variable allocation starting from RAM address 16
- A-instruction and C-instruction translation
- Line-numbered error reporting for invalid instructions

**Test programs:**
- Add.asm
- Max.asm
- Rect.asm
- Pong.asm

All four programs passed comparison against the official assembler output.

## Part C – Box Drawing Program
Created a keyboard-controlled box using Hack Assembly Language.

**Specifications (K = 49):**
- Starting row: 49
- Height: 20 pixels
- Width: 32 pixels
- Starting screen address: 17952

**Functionality:**
- Pressing a key displays a black box.
- Releasing the key clears the box.
- The program continuously checks keyboard input.

The program was assembled using the custom Python assembler and tested in the CPU Emulator.

## Technologies Used
- Hack HDL
- Hack Assembly Language
- Python
- Nand2Tetris CPU Emulator
- VS Code

## Conclusion
This project demonstrates the construction of the Hack computer, implementation of a two-pass assembler, and execution of a keyboard-controlled graphics program using low-level programming concepts.

### Author
Mehul Srivastava
2501730149