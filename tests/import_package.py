'''
    A hack to import pysolo_package for this test directory.
    Using other ways to import wasn't working.
    Was receiving "No known relative parents" error, but this
    solution is working for me.
'''


from pathlib import Path
pysolo_package_dir = Path(__file__).parents[1].absolute()
import sys; sys.path.append(str(pysolo_package_dir))
from pysolo_package import *
