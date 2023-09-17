from src.app import start
import argparse
import sys

parser = argparse.ArgumentParser()
# parser.add_argument("--docker", default=False, action=argparse.BooleanOptionalAction, help="Indicates running from docker container")

if __name__ == '__main__':
    print("Python version:", sys.version)
    args = parser.parse_args([] if "__file__" not in globals() else None)
    start()
