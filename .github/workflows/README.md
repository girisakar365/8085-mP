# GitHub Actions Workflows

## Release Workflow (`release.yml`)

This workflow automates the build and release process for the **8085 Microprocessor Simulator** across all supported platforms.

### Trigger

The workflow is triggered **only when a tag is pushed** matching the pattern `v*`:

```bash
git tag v1.0.0
git push origin v1.0.0
```

> ⚠️ **Note**: Regular pushes to `main` do not trigger this workflow. You must create a tag to initiate a release.
---

### Jobs

#### 1. `build-backend`

Builds the Python backend using **Nuitka** to create standalone binaries.

| Platform | Runner | Output |
|----------|--------|--------|
| Linux | `ubuntu-22.04` | `server` |
| Windows | `windows-latest` | `server.exe` |
| macOS | `macos-latest` | `server` |

**Key Steps:**
- Setup Python 3.12
- Install dependencies from `Backend/requirements.txt`
- Run `Scripts/build.sh` (Unix) or `Scripts/build.ps1` (Windows)
- Upload backend binary as artifact

---

#### 2. `build-tauri`

Builds the Tauri desktop application for all platforms.

| Platform | Runner | Artifacts |
|----------|--------|-----------|
| Linux | `ubuntu-22.04` | `.deb`, `.rpm`, `.AppImage` |
| Windows | `windows-latest` | `.msi`, `.exe` (NSIS) |
| macOS x64 | `macos-latest` | `.dmg` |
| macOS ARM64 | `macos-latest` | `.dmg` (Apple Silicon) |

**Key Steps:**
- Setup Node.js 20
- Setup Rust stable toolchain
- Install platform-specific dependencies
- Download backend artifact from previous job
- Build with `tauri-apps/tauri-action`
- Upload platform installers as artifacts

---

#### 3. `create-release`

Creates a GitHub Release with all built artifacts.

**Key Steps:**
- Download all Tauri artifacts
- Run `Scripts/prepare_release.sh` to collect files
- Create GitHub Release with auto-generated notes
- Upload all installers (`.deb`, `.rpm`, `.AppImage`, `.msi`, `.exe`, `.dmg`)

**Release Naming:**
- Regular releases: `8085 Microprocessor Simulator v1.0.0`
- Pre-releases: Tags containing `alpha`, `beta`, or `rc` are marked as pre-release

---

### Scripts Used

| Script | Platform | Purpose |
|--------|----------|---------|
| `Scripts/build.sh` | Linux/macOS | Build backend with Nuitka |
| `Scripts/build.ps1` | Windows | Build backend with Nuitka |
| `Scripts/prepare_release.sh` | Linux | Collect release artifacts |

---

### How to Create a Release

1. **Update version** in relevant files (`package.json`, `tauri.conf.json`, etc.)

2. **Commit changes**
   ```bash
   git add .
   git commit -m "chore: bump version to 1.0.0"
   ```

3. **Create and push a tag**
   ```bash
   git tag v1.0.0
   git push origin main
   git push origin v1.0.0
   ```

4. **Monitor the workflow** in the Actions tab

5. **Release is created automatically** with all platform installers

---

### Pre-release Tags

Use these suffixes for pre-releases:
- `v1.0.0-alpha.1` - Alpha release
- `v1.0.0-beta.1` - Beta release  
- `v1.0.0-rc.1` - Release candidate

These will be automatically marked as **pre-release** on GitHub.

---

### Required Secrets

| Secret | Description |
|--------|-------------|
| `GITHUB_TOKEN` | Automatically provided by GitHub Actions |

---

### Caching

The workflow uses caching to speed up builds:
- **pip cache**: Python dependencies
- **npm cache**: Node.js dependencies
- **Rust cache**: Cargo dependencies (via `Swatinem/rust-cache`)
