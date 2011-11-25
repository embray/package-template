#!/usr/bin/env python

# Use "distribute" - the setuptools fork that supports python 3.
from distribute_setup import use_setuptools
use_setuptools()

import os
import glob
from setuptools import setup, find_packages
from distutils import log

from astropy import setup_helpers
from astropy.version_helper import get_git_devstr, generate_version_py

packagename = 'packagename'

version = '0.0dev'

# Indicates if this version is a release version
release = 'dev' not in version

# Adjust the compiler in case the default on this platform is to use a
# broken one.
setup_helpers.adjust_compiler()

# Indicate that we are in building mode
setup_helpers.set_build_mode()

if not release:
    version += get_git_devstr(sha=False, path=os.path.abspath(packagename))
generate_version_py(packagename, version, release,
                    setup_helpers.get_debug_option())


# Use the find_packages tool to locate all packages and modules
packagenames = find_packages()

# Treat everything in scripts except README.rst as a script to be installed
scripts = glob.glob('scripts/*')
scripts.remove('scripts/README.rst')

# Check that Numpy is installed.
# NOTE: We cannot use setuptools/distribute/packaging to handle this
# dependency for us, since some of the subpackages need to be able to
# access numpy at build time, and they are configured before
# setuptools has a chance to check and resolve the dependency.
setup_helpers.check_numpy()

# This dictionary stores the command classes used in setup below
cmdclassd = {}

# Additional C extensions that are not Cython-based should be added here.
extensions = []

# A dictionary to keep track of all package data to install
package_data = {packagename: ['data/*']}

# Extra files to install - distutils calls them "data_files", but this
# shouldn't be used for data files - rather any other files that should be
# installed in a special place
data_files = []

setup_helpers.update_package_files(packagename, extensions, package_data,
                                   data_files)

if setup_helpers.HAVE_CYTHON and not release:
    from Cython.Distutils import build_ext
    # Builds Cython->C if in dev mode and Cython is present
    cmdclassd['build_ext'] = build_ext


if setup_helpers.AstropyBuildSphinx is not None:
    cmdclassd['build_sphinx'] = setup_helpers.AstropyBuildSphinx


setup(name=packagename,
      version=version,
      description='Astropy affiliated package',
      packages=packagenames,
      package_data=package_data,
      data_files=data_files,
      ext_modules=extensions,
      scripts=scripts,
      requires=['numpy'],  # scipy not required, but strongly recommended
      install_requires=['numpy'],
      provides=[packagename],
      author='',
      author_email='',
      license='',
      url='http://astropy.org',
      long_description='',
      cmdclass=cmdclassd,
      zip_safe=False,
      use_2to3=True
      )
