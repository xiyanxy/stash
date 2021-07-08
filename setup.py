"""
Setup.py for StaSh on PC.
If you want to install on pythonista instead, run "import requests as r; exec(r.get('https://bit.ly/get-stash').text)"
"""
import ast
import os
import sys


# =================== check if run inside pythonista ===================
IN_PYTHONISTA = sys.executable.find('Pythonista') >= 0

if IN_PYTHONISTA:
    print("您似乎正在使用 pythonista 应用程序运行此文件。")
    print("setup.py 文件用于在 PC 上进行安装。")
    print("请选择以下选项之一：")
    print("[1] 运行 pythonista 特定的安装程序")
    print("[2] 继续安装")
    print("[3] 退出")
    try:
        v = int(input(">"))
    except Exception:
        v = None
    if v == 1:
        # pythonista install
        cmd = "import requests as r; exec(r.get('https://bit.ly/get-stash').text)"
        print('执行: "' + cmd + '"') 
        exec(cmd)
        sys.exit(0)
    elif v == 2:
        # continue
        pass
    else:
        # exit
        if v != 3:
            print("无效输入!")
        print("中止中...")
        sys.exit(1)


# =================== SETUP ===================

from distutils.core import setup
from setuptools import find_packages


TEST_REQUIREMENTS = [
    "pyparsing==2.0.1",
    "pytest>=3.6.0",
    "flake8>=3.5.0",
    "pycrypto==2.6",
    "requests==2.9.1",
]


PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STASH_DIR = os.path.dirname(os.path.abspath(__file__))
CORE_PATH = os.path.join(STASH_DIR, "core.py")
TO_IGNORE = [os.path.abspath(os.path.join(STASH_DIR, p)) for p in ("build", "dist")]


def get_package_data_files(directory, exclude=[]):
    """
    Find data files recursibely.
    Original version from: https://stackoverflow.com/questions/27664504/how-to-add-package-data-recursively-in-python-setup-py
    :param directory: directory to search recursively
    :type directory: str
    :param exclude: list of absolute paths to ignore
    :type exclude: list of str
    :return: package data files to include
    :rtype: list of str
    """
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            fp = os.path.abspath(os.path.join('..', path, filename))
            skip = False
            for v in exclude:
                if fp.startswith(v):
                    skip = True
            if not skip:
                paths.append(fp)
    return paths


def get_stash_version(corepath):
    """
    Find and return the current StaSh version.
    :param corepath: path to the 'core.py' file in the StaSh root directory
    :type corepath: str
    :return: the StaSh version defined in the corepath
    :rtype: str
    """
    with open(corepath, "r") as fin:
        for line in fin:
             if line.startswith("__version__"):
                 version = ast.literal_eval(line.split("=")[1].strip())
                 return version
    raise Exception("在 '{f}' 文件中找不到 StaSh 版本", f=corepath)


# before we start with the setup, we must be outside of the stash root path.
os.chdir(STASH_DIR)
print(STASH_DIR)


setup(
    name="StaSh",
    version=get_stash_version(CORE_PATH),
    description="StaSh for PC",
    author="https://github.com/ywangd and various contributors",
    url="https://github.com/ywangd/stash/",
    packages=[
        "stash",
        "stash.system",
        "stash.system.shui",
        "stash.lib",
    ],
    package_dir={
        "": STASH_DIR,
        "stash": STASH_DIR,
    },
    package_data={
        "": get_package_data_files(STASH_DIR, exclude=TO_IGNORE),
    },
    scripts=[os.path.join(STASH_DIR, "launch_stash.py")],
    zip_safe=False,
    install_requires=[
        "six",      # required by StaSh
        "pyperclip",  # required by libdist for copy/paste on PC
        "requests",
        "pyte",
    ],
    extras_require={
        "testing": TEST_REQUIREMENTS,
    },
)
