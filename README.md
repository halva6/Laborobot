# Laborobot
Control of an old 3D printer, as a lab robot, via the web

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

## Description

Laborobot is a program that aims to repurpose old, broken 3D printers as laboratory robots by controlling them via the web. Using a Scratch-like interface, it is designed to help researchers focus on the essential content of their experiments or research work, rather than on the cumbersome programming of such a robot. This project is being developed as part of a special learning achievement (BeLL).

---

## Project Installation

### Prerequisites

* Python 3.8 or higher
* pip (Python package manager)
* Git

---

## Option 1: Automatic Setup (Recommended)

A `bootstrap.py` script is provided to automatically create the virtual environment and install all required dependencies.

1. **Clone the repository**

   ```bash
   git clone https://github.com/halva6/Laborobot.git
   cd Laborobot
   ```

2. **Run the bootstrap script**

   ```bash
   python bootstrap.py
   ```

   This script will:
   * Create a virtual environment (`.venv/`)
   * Activate it automatically
   * Install all dependencies listed in `requirements.txt`

3. **Start the application**

   * For **development** (Flask’s built-in server):
     ```bash
     python flaskr/app.py
     ```

   * For **production** (Gunicorn with WebSocket support):

     ```bash
     cd flaskr
     gunicorn -k eventlet -w 1 -b 0.0.0.0:5000 app:app
     ```

4. **Access the web interface**
   Open your browser and navigate to:

   ```
   http://localhost:5000
   ```

   or, if hosted remotely:

   ```
   http://<your-server-ip>:5000
   ```

---

## Option 2: Manual Installation

If you prefer to install dependencies manually, follow these steps:

1. **Clone the repository**

   ```bash
   git clone https://github.com/halva6/Laborobot.git
   cd Laborobot
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**

   * On Windows:

     ```bash
     .venv\Scripts\activate
     ```
   * On macOS/Linux:

     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**

   * Development server:

     ```bash
     python flaskr/app.py
     ```
   * Production server:

     ```bash
     gunicorn -k eventlet -w 1 -b 0.0.0.0:5000 flaskr.app:app
     ```

6. **Access the web interface**
   Open your browser and go to:

   ```
   http://localhost:5000
   ```
