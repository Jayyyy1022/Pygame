import sys
import os
import subprocess

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
menu_path = os.path.join(ROOT_DIR, "Scenes", "menu.py")

print("Starting Good Night, Sleep Tight...")

subprocess.run([sys.executable, menu_path])

sys.exit()