# 📦 Project Setup

---

# 🎥 Demo Video

**See the application in action:**  
[▶️ Watch the Demo Video on Google Drive](https://drive.google.com/file/d/1v6O5MZQ3HZGXIjKejOmeEpgnVUDPGmH9/view?usp=sharing)

This video demonstrates the main features, user flows, and UI of the project.

---

# 🧩 1. Install Homebrew (Mac Only)

> Skip this step if you're on Windows.

Homebrew is a package manager for macOS.  
You’ll use it to easily install Git, Python, Docker, etc.

**Install Homebrew:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Verify Homebrew:**

```bash
brew --version
```

If you see a version number, you're good to go.

---

# 🧩 2. Install and Configure Git

## Install Git

- **MacOS (using Homebrew)**

```bash
brew install git
```

- **Windows**

Download and install [Git for Windows](https://git-scm.com/download/win).  
Accept the default options during installation.

**Verify Git:**

```bash
git --version
```

---

## Configure Git Globals

Set your name and email so Git tracks your commits properly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Confirm the settings:

```bash
git config --list
```

---

## Generate SSH Keys and Connect to GitHub

> Only do this once per machine.

1. Generate a new SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

(Press Enter at all prompts.)

2. Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

3. Add the SSH private key to the agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

4. Copy your SSH public key:

- **Mac/Linux:**

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

- **Windows (Git Bash):**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

5. Add the key to your GitHub account:
   - Go to [GitHub SSH Settings](https://github.com/settings/keys)
   - Click **New SSH Key**, paste the key, save.

6. Test the connection:

```bash
ssh -T git@github.com
```

You should see a success message.

---

# 🧩 3. Clone the Repository

Now you can safely clone the course project:

```bash
git clone <repository-url>
cd <repository-directory>
```

---

# 🛠️ 4. Install Python 3.10+

## Install Python

- **MacOS (Homebrew)**

```bash
brew install python
```

- **Windows**

Download and install [Python for Windows](https://www.python.org/downloads/).  
✅ Make sure you **check the box** `Add Python to PATH` during setup.

**Verify Python:**

```bash
python3 --version
```
or
```bash
python --version
```

---

## Create and Activate a Virtual Environment

(Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate.bat  # Windows
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

---

# 🐳 5. (Optional) Docker Setup

> Skip if Docker isn't used in this module.

## Install Docker

- [Install Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- [Install Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

## Build Docker Image

```bash
docker build -t <image-name> .
```

## Run Docker Container

```bash
docker run -it --rm <image-name>
```

---

# 🚀 6. Running the Project

- **Without Docker**:

```bash
python main.py
```

(or update this if the main script is different.)

- **With Docker**:

```bash
docker run -it --rm <image-name>
```

---

# 📝 7. Submission Instructions

After finishing your work:

```bash
git add .
git commit -m "Complete Module X"
git push origin main
```

Then submit the GitHub repository link as instructed.

---

# 🔥 Useful Commands Cheat Sheet

| Action                         | Command                                          |
| ------------------------------- | ------------------------------------------------ |
| Install Homebrew (Mac)          | `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |
| Install Git                     | `brew install git` or Git for Windows installer |
| Configure Git Global Username  | `git config --global user.name "Your Name"`      |
| Configure Git Global Email     | `git config --global user.email "you@example.com"` |
| Clone Repository                | `git clone <repo-url>`                          |
| Create Virtual Environment     | `python3 -m venv venv`                           |
| Activate Virtual Environment   | `source venv/bin/activate` / `venv\Scripts\activate.bat` |
| Install Python Packages        | `pip install -r requirements.txt`               |
| Build Docker Image              | `docker build -t <image-name> .`                |
| Run Docker Container            | `docker run -it --rm <image-name>`               |
| Push Code to GitHub             | `git add . && git commit -m "message" && git push` |

---

# 📋 Notes

- Install **Homebrew** first on Mac.
- Install and configure **Git** and **SSH** before cloning.
- Use **Python 3.10+** and **virtual environments** for Python projects.
- **Docker** is optional depending on the project.

---

# 📎 Quick Links

- [Homebrew](https://brew.sh/)
- [Git Downloads](https://git-scm.com/downloads)
- [Python Downloads](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

---

# ✨ User Profile & Password Change Feature

This application now supports user profile management and secure password changes.

## Features

- View and update your profile (first name, last name, username, email)
- Change your password securely (old password required)
- All changes require authentication (JWT)
- Frontend at `/profile` for profile and password management

---

# 🧮 Additional Calculation Type: Exponentiation

The calculator now supports exponentiation (`base ** exponent`).

- Select "Exponentiation" in the operation dropdown on the dashboard.
- Enter two numbers: the base and the exponent (e.g., `2, 8` for $2^8$).
- Result is computed and shown in the calculation history.

## API Example

```json
{
  "type": "exponentiation",
  "inputs": [2, 8]
}
```

Result: `256`

---

# 📊 Report/History Feature

The dashboard now displays usage statistics for your calculations:

- **Total Calculations:** Number of calculations performed.
- **Average Operands:** Average number of numbers used per calculation.
- **Most Common Type:** Most frequently used calculation type.
- **Last Calculation:** Date/time of the most recent calculation.

## API Example

- `GET /calculations/report` — Returns a summary of your calculation usage:

```json
{
  "total_calculations": 5,
  "average_operands": 2.4,
  "most_common_type": "addition",
  "last_calculation_at": "2025-12-15T17:00:00"
}
```

## Frontend Usage

- Go to `/dashboard` to view your usage metrics at the top of the page.
- Metrics update automatically as you perform calculations.

---

## API Endpoints

- `GET /users/me` — Get current user's profile (JWT required)
- `PUT /users/me` — Update profile fields (JWT required)
- `POST /users/me/change-password` — Change password (JWT required)
- `POST /calculations` — Create a calculation (supports exponentiation)
- `GET /calculations/report` — Get calculation usage stats (JWT required)

## Frontend Usage

- Go to `/profile` after logging in to view or update your profile and change your password.
- Go to `/dashboard` to perform calculations, including exponentiation and view usage metrics.
- All changes are validated client-side and server-side.
- You must be logged in; JWT is stored in localStorage after login.

## Running Tests

- **Unit tests:**  
  `pytest tests/unit/`
- **Integration tests:**  
  `pytest tests/integration/`
- **E2E tests (Playwright):**  
  `pytest tests/e2e/`  
  (Requires Playwright and a running server)

---

# 🐳 Docker Hub Image

The latest Docker image for this project is available at:

[https://hub.docker.com/repository/docker/varuns03/is601-assignment-14/tags](https://hub.docker.com/repository/docker/varuns03/is601-assignment-14/tags)

Pull the image:

```bash
docker pull varuns03/is601-assignment-14:latest
```
