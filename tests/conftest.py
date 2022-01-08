import sys
from os.path import abspath, dirname, join


WORKSPACE = dirname(dirname(abspath(__file__)))
SCRIPT_DIR = join(WORKSPACE, "src")
sys.path.append(SCRIPT_DIR)
