# Contributing to ASM Studio

Welcome! We're excited that you're interested in contributing to ASM Studio. This document outlines the process for contributing to this project.

## Code of Conduct

This project has adopted a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Asking Questions

Have a question? Open a GitHub issue with the `question` label.

## Reporting Issues

Before creating an issue, please search existing issues to avoid duplicates.

When reporting a bug, include:

- Steps to reproduce the behavior
- Expected behavior vs actual behavior
- Your environment (OS, Python version, Node version, Rust version)
- Relevant error messages or logs

## Contributing Code

### Prerequisites

- Python 3.12+
- Node.js 22+
- Rust 1.70+
- Git

### Setup

1. Fork and clone the repository:

   ```bash
   git clone https://github.com/YOUR-USERNAME/8085-mP.git
   cd 8085-Microprocessor
   git remote add upstream https://github.com/girisakar365/8085-mP.git
   ```

2. Run the setup script:

   ```bash
   # Linux/macOS
   ./Scripts/dev.sh

   # Windows
   .\Scripts\dev.bat
   ```

3. Create a branch for your changes:

   ```bash
   git checkout -b my-feature
   ```

### Making Changes

1. Make your changes
2. Test your changes
3. Commit using [Conventional Commits](https://www.conventionalcommits.org/) format:

   ```bash
   git commit -m "feat(parser): add support for comments"
   git commit -m "fix(memory): resolve overflow issue"
   git commit -m "docs: update setup instructions"
   ```

### Submitting a Pull Request

1. Push your branch to your fork:

   ```bash
   git push origin my-feature
   ```

2. Open a pull request against the `main` branch
3. Fill in the PR template with a clear description of your changes
4. Wait for review and address any feedback

## Coding Guidelines

### Python

- Follow [PEP 8](https://pep8.org/)
- Use type hints
- Write docstrings for public functions

### JavaScript/React

- Use functional components with hooks
- Use descriptive variable and function names

### General

- Write self-documenting code
- Add comments for complex logic
- Write tests for new features

## Testing

```bash
# Run specific tests
python -m Test.Commands.arithmetic
```

## Thank You

Your contributions help make ASM Studio better for everyone.

Last updated: November 2025
