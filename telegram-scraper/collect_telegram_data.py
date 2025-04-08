from pathlib import Path


def main():
    current_directory = Path.cwd()
    for i in current_directory.iterdir():
        csv_file = next(i.rglob('*'))