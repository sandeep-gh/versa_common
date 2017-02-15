import glob
import os

def get_last_file_by_pattern(pattern=None):
    files = glob.glob(pattern)
    if not files:
        return None
    if files:
        files.sort(key=os.path.getmtime)
        return files[-1]
