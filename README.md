# Laborobot
Control of an old 3D printer, as a lab robot, via the web

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

## Description

Laborobot is a program that aims to repurpose old, broken 3D printers as laboratory robots by controlling them via the web. Using a Scratch-like interface, it is designed to help researchers focus on the essential content of their experiments or research work, rather than on the cumbersome programming of such a robot. This project is being developed as part of a special learning achievement (BeLL).

## Project Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/halva6/Laborobot.git
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000` or to `http://127.0.0.1:5000`

### Troubleshooting

- If you get port conflicts, use a different port:
  ```bash
  flask run --port 5001
  ```

- If requirements.txt is missing, install Flask manually:
  ```bash
  pip install flask
  ```

- Make sure your virtual environment is activated before installing dependencies