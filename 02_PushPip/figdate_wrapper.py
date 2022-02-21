import os
import sys
import venv
import subprocess as sp
from tempfile import TemporaryDirectory

with TemporaryDirectory() as tmp_dir:
    venv.create(tmp_dir, with_pip=True)
    
    pip_path = os.path.join(tmp_dir, "bin/pip")
    py_path = os.path.join(tmp_dir, "bin/python")

    ret = sp.run([pip_path, "install", "pyfiglet"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
    if ret.returncode != 0:
        raise RuntimeError("Pip failed to execute")

    sp.run([py_path, "-m", "figdate"] + sys.argv[1:])
    if ret.returncode != 0:
        raise RuntimeError("Package failed to execute")

