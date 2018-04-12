#!/usr/bin/env python3
"""Run all the chapter modules, doctests or performance() function

This is run from the top-level directory, where all of the sample
data files are also located.

When runnning individual examples, working directory is expected
to be this top-level directory.
"""
import doctest
import os
import glob
import runpy
import unittest
import sys
import time
import importlib

DEBUG = False # Can't easily use logging -- conflict with Chapter_11

def package_module_iter(*packages):
    """For a given list of packages, emit the package name and a generator
    for all modules in the package. Structured like ``itertools.groupby()``.
    """
    def module_iter(package, module_iter):
        if DEBUG:
            print("Package {0}".format(package))
        for filename in module_iter:
            basename = os.path.split(filename)[-1]
            module, ext = os.path.splitext(basename)
            if (
                    module.startswith("__")
                    and module.endswith("__")
                    and ext == ".py"):
                continue
            if DEBUG:
                print("  file {0} module {1}".format(basename, module))
            yield basename, module

    for package in packages:
        yield (package,
               module_iter(package, glob.glob(os.path.join(package,"*.py"))))

def run(pkg_mod_iter):
    """Run each module."""
    for package, module_iter in pkg_mod_iter:
        print(package)
        print("="*len(package))
        print()
        for filename, module in module_iter:
            runpy.run_path(package+"/"+filename, run_name="__main__")

def run_test_suite(pkg_mod_iter):
    """Doctest each module individually.

    Might be simpler to use subprcoess.run(['python3', '-m', 'doctest', module])
    """
    for package, module_iter in pkg_mod_iter:
        print(package)
        print("="*len(package))
        print()
        for filename, module in module_iter:
            suite = doctest.DocTestSuite(package+"."+module)
            runner = unittest.TextTestRunner(verbosity=1)
            runner.run(suite)

def run_performance(pkg_mod_iter):
    """Locate a performance() function in each module and run it."""
    for package, module_iter in pkg_mod_iter:
        print(package)
        print("="*len(package))
        print()
        for filename, modname in module_iter:
            print(filename, modname)
            try:
                module = __import__(
                    package+"."+modname, fromlist=(modname, "performance"))
                module.performance()
            except AttributeError:
                pass # no performance() function in the module.

def master_test_suite(pkg_mod_iter):
    """Build a master test suite from all modules and run that."""
    master_suite = unittest.TestSuite()
    for package, module_iter in pkg_mod_iter:
        for filename, module in module_iter:
            print(package+"."+module, file=sys.stderr)
            suite = doctest.DocTestSuite(package+"."+module)
            print("  ", suite, file=sys.stderr)
            master_suite.addTests(suite)
    runner = unittest.TextTestRunner(verbosity=1)
    runner.run(master_suite)

def chap_key(name: str) -> int:
    _, _, n = name.partition("_")
    return int(n)

if __name__ == "__main__":
    content = sorted(glob.glob("Chapter_*"), key=chap_key)
    if DEBUG:
        print(content, file=sys.stderr)
    master_test_suite(package_module_iter(*content))
