import subprocess

if __name__ == '__main__':
    python_bin = "venv/Scripts/python"
    script_file = "main.py"

    p = subprocess.Popen([python_bin, script_file])
    p.wait()    # remove, tests only
