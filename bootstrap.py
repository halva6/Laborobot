import sys
import subprocess
import os
from pathlib import Path

VENV_DIR = Path(".venv")  # or whatever your venv path is
REQ_FILE = Path("requirements.txt")


def run(cmd):
    """Run a command and print it."""
    print(f"→ {' '.join(map(str, cmd))}")
    subprocess.check_call(cmd)


def main():
    """Main function to set up virtual environment and install dependencies."""
    python = sys.executable

    # create virtual environment if it doesn't exist
    if not VENV_DIR.exists():
        print(f"Creating virtual environment in {VENV_DIR}...")
        run([python, "-m", "venv", str(VENV_DIR)])

    venv_python = VENV_DIR / ("Scripts" if os.name == "nt" else "bin") / "python"
    venv_pip = [str(venv_python), "-m", "pip"]

    # upgrade pip - but use python from venv to do so
    run(venv_pip + ["install", "--upgrade", "pip"])

    # install requirements if the file exists
    if REQ_FILE.exists():
        run(venv_pip + ["install", "-r", str(REQ_FILE)])
    else:
        print(f"⚠️ No {REQ_FILE} found.")

    activate_cmd = (
        f"{VENV_DIR}\\Scripts\\activate"
        if os.name == "nt"
        else f"source {VENV_DIR}/bin/activate"
    )
    print(f"\n✅ Virtual environment ready! Activate it with:\n   {activate_cmd}")


if __name__ == "__main__":
    main()
