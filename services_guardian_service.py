# Guardian Service - Auto-Audit Daemon
import time
import subprocess

class GuardianService:
    def __init__(self, pipeline_path: str, interval: int = 3600):
        self.pipeline_path = pipeline_path
        self.interval = interval

    def run(self):
        while True:
            print(f"Running self-audit pipeline: {self.pipeline_path}")
            subprocess.run(["glyphnet", "run", self.pipeline_path])
            time.sleep(self.interval)
