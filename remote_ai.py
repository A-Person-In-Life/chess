from pathlib import Path
import os
import subprocess
import sys

class RemoteAI:
    def __init__(self, depth=2, workers=4):
        python_t = "python3.14t"
        worker_script = (Path(__file__).resolve().with_name("ai.py"))

        env = os.environ.copy()
        env["PYTHON_GIL"] = "0"
        self.process = subprocess.Popen([python_t, ])