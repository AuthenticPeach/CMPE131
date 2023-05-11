import os
import sys
import subprocess

def main():
    requirements_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")
    subprocess.call([sys.executable, "-m", "pip", "install", "-r", requirements_path])

if __name__ == "__main__":
    main()
