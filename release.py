import os
import shutil
import tarfile

from eznotes.const import VERSION


RELEASE_NAME = f"eznotes-{VERSION}.tar.gz"
FILES_TO_ADD = ["LICENSE", "README.md", "setup.py"]

os.mkdir("tar")
os.system("cp -r eznotes tar")

with open("tar/eznotes/const.py") as f:
    const_file = f.read()

# Turning debug mode off
with open("tar/eznotes/const.py", "w") as f:
    f.write(const_file.replace("DEBUG = True", "DEBUG = False"))


with tarfile.open(RELEASE_NAME, "w:gz") as tar:
    for filename in FILES_TO_ADD:
        tar.add(filename)
    # Adding the changed eznotes dir
    os.chdir("tar")
    tar.add("eznotes")

# cleaning up
os.chdir("..")
shutil.rmtree("tar")
