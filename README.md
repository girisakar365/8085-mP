# 8085 Microprocessor Simulator CLI

Welcome to the 8085 Microprocessor Simulator Command Line Interface (CLI)!

## Overview

This project is a command line interface (CLI) for simulating the 8085 microprocessor. The simulator provides a convenient way to interact with an emulated 8085 microprocessor, allowing you to execute instructions and observe the state of the microprocessor, including registers, memory, flags, and more.

## Features

- Execute a variety of 8085 instructions, such as MOV, MVI, LXI, LDA, STA, ADD, SUB, INR, DCR, and many more.
- View the contents of registers, memory, flags, ports, and other components of the 8085 microprocessor.
- Clear the console screen for a clean and organized interface.
- Explore the state of the microprocessor through commands like `exmin_memory`, `exmin_port`, `exmin_memol`, `exmin_register`, and `exmin_flag`.

## Getting Started

### Prerequisites

Before running the simulator, ensure that you have the required Python modules installed. You can install them using the following command:

```bash
pip install prettytable
```

### Running the Simulator
1. Clone the repository:
```bash
https://github.com/girisakar365/8085-mP.git
```
2. Navigate to the project directory:
```bash
cd 8085-mP
```
3. Run the CLI:
```bash
python CLI.py
```

## Usage
1. After launching the simulator, you will be greeted with an introduction and the command prompt (> ).

2. Enter 8085 microprocessor instructions to execute various operations. For example:
```bash
> MOV A, B
```
3. Use the help command to view the list of available commands and their descriptions:

```bash
> help
```
4. Explore the state of the microprocessor using commands like exmin_memory, exmin_port, exmin_memol, exmin_register, and exmin_flag.

5. Clear the console screen with the clear or cls command for a clean interface:
```bash
> clear
```
### Note
1. __As of now, not all instructions are available (available upto logical operators), and updates are constantly being made. Instructions up to arithmetic operations are supported__.
2. __None of the flags are effected if any such operations are performed.__
2. Ensure that you provide valid arguments and follow the correct syntax for each instruction. For additional information on specific commands, use the help command followed by the command name. For example:
```bash
> help MOV
```

## Supported Platforms
The simulator is compatible with Windows, Linux, and macOS.

- Windows: No additional considerations.
- Linux: Ensure you have the necessary dependencies by running the command mentioned under [Prerequisites.](#prerequisites)
- macOS: Similar to Linux, ensure the required dependencies are installed.

## Currently Working On:
1. Flag modification `main`
1. Branching Group `main`
2. AI integration
2. Stack Group

## Contributing
Feel free to contribute to the project by opening issues or submitting pull requests. Your feedback and contributions are highly appreciated. Happy coding!