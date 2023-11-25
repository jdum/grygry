import subprocess
from pathlib import Path

DATA = Path(__file__).parent / "data"


def capture(command: list[str], working_directory: Path) -> tuple:
    proc = subprocess.Popen(
        command,
        cwd=working_directory,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out.decode().strip(), err.decode().strip(), proc.returncode


def test_no_param1():
    command = ["grypy"]
    out, err, exitcode = capture(command, DATA)
    assert exitcode == 1
    assert out == ""
    assert "NoPatternError" in err


def test_no_param2():
    command = ["gryrb"]
    out, err, exitcode = capture(command, DATA)
    assert exitcode == 1
    assert out == ""
    assert "NoPatternError" in err


def test_grypy_1():
    command = ["grypy", "self.found"]
    out, err, exitcode = capture(command, DATA)
    assert exitcode == 0
    assert err == ""
    assert "grylib.py" in out
    assert "grylib_copie.py" in out
    assert "subdir" in out
    assert "20:         self.path = Path()" in out
    assert "21:         self.found = {}" in out
    assert "22:" in out


def test_grypy_2():
    command = ["grypy", "self.found"]
    out, err, exitcode = capture(command, DATA / "subdir")
    assert exitcode == 0
    assert err == ""
    assert "grylib.py" not in out
    assert "grylib_copie.py" in out
