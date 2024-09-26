import sys
from cx_Freeze import setup, Executable
buildOptions = dict(packages = ['datetime', 'selenium', 'webdriver_manager'], excludes = ["scipy.spatial.cKDTree"], include_files=['config.json'])
exe = [Executable("traffic.py")]
setup(name= 'Filter', version = '0.1', author = "KSTAT", description = "KOPIS traffic", options = dict(build_exe = buildOptions), executables = exe)
