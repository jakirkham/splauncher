from __future__ import print_function


__author__ = "John Kirkham <kirkhamj@janelia.hhmi.org>"
__date__ = "$May 18, 2015 12:09:31 EDT$"


from glob import glob
import os
import shutil
import sys

from setuptools import setup, find_packages


build_requires = []
install_requires = []
tests_require = ["nose"]
sphinx_build_pdf = False
if len(sys.argv) == 1:
    pass
elif ("--help" in sys.argv) or ("-h" in sys.argv):
    pass
elif sys.argv[1] == "bdist_conda":
    tests_require = [
        "nose"
    ]
elif sys.argv[1] == "build_sphinx":
    import sphinx.apidoc

    sphinx.apidoc.main([
        sphinx.apidoc.__file__,
        "-f", "-T", "-e", "-M",
        "-o", "docs",
        ".", "setup.py", "tests", "versioneer.py"
    ])

    build_prefix_arg_index = None
    for each_build_arg in ["-b", "--builder"]:
        try:
            build_arg_index = sys.argv.index(each_build_arg)
        except ValueError:
            continue

        if sys.argv[build_arg_index + 1] == "pdf":
            sphinx_build_pdf = True
            sys.argv[build_arg_index + 1] = "latex"

elif sys.argv[1] == "clean":
    saved_rst_files = ["docs/index.rst", "docs/readme.rst", "docs/todo.rst"]

    tmp_rst_files = glob("docs/*.rst")

    print("removing 'docs/*.rst'")
    for each_saved_rst_file in saved_rst_files:
        print("skipping '" + each_saved_rst_file + "'")
        tmp_rst_files.remove(each_saved_rst_file)

    for each_tmp_rst_file in tmp_rst_files:
        os.remove(each_tmp_rst_file)

    if os.path.exists("build/sphinx/doctrees"):
        print("removing 'build/sphinx/doctrees'")
        shutil.rmtree("build/sphinx/doctrees")
    else:
        print("'build/sphinx/doctrees' does not exist -- can't clean it")

    if (len(sys.argv) > 2) and (sys.argv[2] in ["-a", "--all"]):
        if os.path.exists("build/sphinx"):
            print("removing 'build/sphinx'")
            shutil.rmtree("build/sphinx")
        else:
            print("'build/sphinx' does not exist -- can't clean it")

setup(
    name="subprocess-launcher",
    version="",
    description="A simple subprocess launcher with optional DRMAA support.",
    url="https://github.com/jakirkham/subprocess-launcher",
    license="BSD",
    author="John Kirkham",
    author_email="kirkhamj@janelia.hhmi.org",
    scripts=glob("bin/*"),
    packages=find_packages(exclude=["tests*"]),
    build_requires=build_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite="nose.collector",
    zip_safe=True
)