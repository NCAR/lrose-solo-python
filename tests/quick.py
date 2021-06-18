import os
from pathlib import Path


path_to_file = Path.cwd() / Path('src/pysolo_package/libs/solo.dll')

print(path_to_file)

# dirname = os.path.dirname(os.path.abspath(__file__))
# libraryName = os.path.join(dirname, 'libs/solo.dll')
# print(libraryName)
