import sys
import os

# Get the parent folder path
parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the parent folder to sys.path
sys.path.append(parent_folder)


from buildozer import Buildozer

def test_buildozer():
    workspace = parent_folder + "/../../../example/" # TODO: change if refactoring and fodler movement
    bldz = Buildozer("buildozer")

    # add new file into src
    bldz.execute_cmd(workspace, "//main:hello-greet", Buildozer.Command.add("srcs", "new_file1.cpp"))

test_buildozer()

