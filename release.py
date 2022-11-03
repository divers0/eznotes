import os
import shutil
import tarfile

from eznotes.const import VERSION

try:
    os.mkdir("build")
except FileExistsError:
    shutil.rmtree("build")
    os.mkdir("build")

os.chdir("build")

THIS_VERSION_NAME = f"eznotes-{VERSION}"
RELEASE_PATH = f"{THIS_VERSION_NAME}.tar.gz"
FILES_TO_ADD = ["LICENSE", "README.md", "setup.py"]

os.mkdir(THIS_VERSION_NAME)
os.system(f"cp -r ../eznotes {THIS_VERSION_NAME}")

for file in FILES_TO_ADD:
    os.system(f"cp ../{file} {THIS_VERSION_NAME}")

with open(f"{THIS_VERSION_NAME}/eznotes/const.py") as f:
    const_file = f.read()

# Turning debug mode off
with open(f"{THIS_VERSION_NAME}/eznotes/const.py", "w") as f:
    f.write(const_file.replace("DEBUG = True", "DEBUG = False"))


with tarfile.open(RELEASE_PATH, "w:gz") as tar:
    tar.add(THIS_VERSION_NAME)

# cleaning up
shutil.rmtree(THIS_VERSION_NAME)
