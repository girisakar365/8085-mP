# ASM Studio - 8085 Microprocessor Simulator

[![License](https://img.shields.io/badge/License-Non--Commercial-blue.svg)](LICENSE.md)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Node.js](https://img.shields.io/badge/Node.js-22+-339933?logo=node.js&logoColor=white)](https://nodejs.org)
[![Rust](https://img.shields.io/badge/Rust-1.70+-000000?logo=rust&logoColor=white)](https://rust-lang.org)

ASM Studio is an open-source simulator for the Intel 8085 microprocessor. It provides an interface to write, assemble, and execute 8085 assembly programs while observing the complete state of the processor including registers, memory, flags, and I/O ports.

## Prerequisites

You need the following tools installed on your system:

- [Python](https://python.org/downloads) 3.12 or later
- [Node.js](https://nodejs.org) 22 or later (includes npm)
- [Rust](https://rustup.rs) 1.70 or later (includes Cargo) — for more info visit [rust-lang.org](https://www.rust-lang.org/tools/install)
- [Git](https://git-scm.com)

## System Dependencies

### Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install libwebkit2gtk-4.1-dev build-essential curl wget file \
  libssl-dev libgtk-3-dev libayatana-appindicator3-dev librsvg2-dev
```

### Linux (Arch)

```bash
sudo pacman -S webkit2gtk-4.1 base-devel curl wget file openssl gtk3 \
  libappindicator-gtk3 librsvg
```

### macOS

Install Xcode Command Line Tools:

```bash
xcode-select --install
```

### Windows

Install [Microsoft Visual Studio C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/). When installing, select **Desktop development with C++**.

## Development

### Quick Setup

```bash
git clone https://github.com/girisakar365/8085-mP.git
cd 8085-mP

# Linux/macOS
chmod +x Scripts/dev.sh
./Scripts/dev.sh

# Windows
.\Scripts\dev.bat
```

### Manual Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/girisakar365/8085-mP.git
   cd 8085-mP
   ```

2. **Setup Backend**

   ```bash
   cd Backend
   python3 -m venv .venv
   source .venv/bin/activate    # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   cd ..
   ```

3. **Setup Frontend**

   ```bash
   npm ci
   ```

## Running

```bash
python -m Server
npm run tauri dev
```

For web-only development (without Tauri):

```bash
npm run dev
```

### Build

```bash
npm run tauri build
```

## Dev Containers

This repository includes a [Dev Container](https://containers.dev) configuration for Visual Studio Code. This provides a consistent development environment with all dependencies pre-installed.

To use:

1. Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Open the repository in VS Code
3. Click "Reopen in Container" when prompted (or run `Dev Containers: Reopen in Container` from the command palette)

The container will automatically run the setup script on creation.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## Code of Conduct

This project has adopted a [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before participating.

## License

This project is licensed under a Non-Commercial License. See [LICENSE.md](LICENSE.md) for details.

Last Updated: November 2025