# Development Environment Setup: Python & Pygame

This guide provides instructions to set up the Python programming environment and the Pygame library for the module Developing a Sustainability Tower Defense Game for De Vinci International Week.

---

## 1. Windows Setup

### Step 1: Install Python
1. Download the latest stable installer from [python.org](https://www.python.org/downloads/).
2. Run the installer.
3. **CRITICAL:** Check the box **"Add Python to PATH"** at the bottom of the installer before clicking **Install Now**.

### Step 2: Install Pygame
Open **Command Prompt (cmd)** or **PowerShell** and run:
```bash
pip install pygame
```

## 2. macOS Setup

### Step 0: Install Homebrew
macOS does not come with a package manager by default. Homebrew is essential for managing software packages.

1. Open **Terminal**.
2. Copy and paste the following command:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Note: After the installation completes, check the Terminal output for "Next steps". You will need to run 2-3 commands provided there to add Homebrew to your PATH.

### Step 1: Install Python
brew install python

### Step 2: Install Pygame
pip3 install pygame
