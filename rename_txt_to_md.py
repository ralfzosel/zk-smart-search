# helper utility, that renames all files in folder ZK_BASE_DIR with ending .txt to .md
# run this script from the root folder of this project
# e.g. python scripts/rename_txt_to_md.py

import os
import glob
from settings import ZK_BASE_DIR

for filename in glob.glob(os.path.join(ZK_BASE_DIR, "*.txt")):
    new_filename = filename[:-4] + ".md"
    os.rename(filename, new_filename)
    print(f"renamed {filename} to {new_filename}")
