import subprocess
import sys

subprocess.run([sys.executable, "-m", "PyInstaller", "--onefile", "--name", "app", "app.py"], check=True)
print("Built dist/app.exe")
