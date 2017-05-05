from flake8.api import legacy as flake8
import subprocess
import os

cwd = os.getcwd()


def build_path(*args):
    return os.path.join(*args)


def run_flake8(paths):
    """Runs flake8 linter"""

    style = flake8.get_style_guide()
    report = style.check_files([paths])
    codes = ['E', 'F', 'W', 'C90']
    for code in codes:
        if report.get_statistics(code):
            exit(1)


def run_unittest(path, warning):
    """Recursively discovers unittest modules in the
    specified path and runs them
    """

    cmd = 'python3 -m unittest discover'.split(' ')

    if not warning:
        cmd.insert(1, '-W')
        cmd.insert(2, 'ignore')

    subprocess.call([*cmd, path])


if __name__ == '__main__':
    flake8_path = build_path(cwd, 'ica')
    unittest_path = build_path(cwd, 'ica', 'tests')

    print('Running flake8')
    run_flake8(flake8_path)

    print('Running unittest')
    run_unittest(unittest_path, False)

    exit(0)
