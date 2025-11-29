# 8085 Microprocessor Simulator

Welcome to the 8085 Microprocessor Simulator!

## Overview

This project is for simulating the 8085 microprocessor. The simulator provides a convenient way to interact with an emulated 8085 microprocessor, allowing you to execute instructions and observe the state of the microprocessor, including registers, memory, flags, and more.

Main branch contains the core backend logic for the simulator. Here we update the backend and test new features before merging them into the stable CLI OR APP Branch.

## Features

- Execute all of 8085 instructions, such as MOV, MVI, LXI, LDA, STA, ADD, SUB, INR, DCR, and many more.
- View the contents of registers, memory, flags, ports, and other components of the 8085 microprocessor.

## Getting Started

Clone the repository.
```bash
git clone git@github.com:girisakar365/8085-mP.git
```

### Prerequisites

Before running the Packages, ensure that you have the required Python modules installed. You can install them using the following command:

```bash
pip install -r requirements.txt
```
## Checklist:
- Test cases Programs added: 54
- Tests on Parser, Assembler.
- Core logic implementation on subroutine and branching statements.
- ORG and DB implementation.
- API development

## Working On:
- Adding Frontend
- Adding test cases for every features of M8085.

## Contributing
- Fork the repository.
- Create your feature branch: `git checkout -b feature/YourFeature`
- Commit your changes: `git commit -m 'Add some YourFeature'`
- Push to the branch: `git push origin feature/YourFeature`
- Open a pull request.

## License
This project is licensed under  [LICENSE](LICENSE). Check the file for details.