# Setup script for cython template

import io
import os
import re
import sys
import subprocess


PACKAGE_NAME = 'cython_template'
DESCRIPTION = "cython_template: Template for Packages using Cython"
LONG_DESCRIPTION = DESCRIPTION
AUTHOR = "Jake VanderPlas"
AUTHOR_EMAIL = "jakevdp@uw.edu"
URL = 'https://github.com/jakevdp/cython_template'
DOWNLOAD_URL = 'https://github.com/jakevdp/cython_template'
LICENSE = 'BSD 2-clause'


def read(path, encoding='utf-8'):
    path = os.path.join(os.path.dirname(__file__), path)
    with io.open(path, encoding=encoding) as fp:
        return fp.read()


def version(package):
    """Obtain the packge version from a python file e.g. pkg/__init__.py

    See <https://packaging.python.org/en/latest/single_source_version.html>.
    """
    version_file = read(os.path.join(package, '__init__.py'))
    print(version_file)
    version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def generate_cython(package):
    cwd = os.path.abspath(os.path.dirname(__file__))
    print("Cythonizing sources")
    p = subprocess.call([sys.executable,
                         os.path.join(cwd, 'tools', 'cythonize.py'),
                         package],
                        cwd=cwd)
    if p != 0:
        raise RuntimeError("Running cythonize failed!")


def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage(PACKAGE_NAME)

    return config


def setup_package():
    from numpy.distutils.core import setup

    old_path = os.getcwd()
    local_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    src_path = local_path

    os.chdir(local_path)
    sys.path.insert(0, local_path)

    # Run build
    old_path = os.getcwd()
    os.chdir(src_path)
    sys.path.insert(0, src_path)

    cwd = os.path.abspath(os.path.dirname(__file__))
    if not os.path.exists(os.path.join(cwd, 'PKG-INFO')):
        # Generate Cython sources, unless building from source release
        generate_cython(PACKAGE_NAME)

    try:
        setup(name=PACKAGE_NAME,
              author=AUTHOR,
              author_email=AUTHOR_EMAIL,
              url=URL,
              download_url=DOWNLOAD_URL,
              description=DESCRIPTION,
              long_description = LONG_DESCRIPTION,
              version=version(PACKAGE_NAME),
              license=LICENSE,
              configuration=configuration,
              classifiers=[
                'Development Status :: 4 - Beta',
                'Environment :: Console',
                'Intended Audience :: Science/Research',
                'License :: OSI Approved :: BSD License',
                'Natural Language :: English',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3.4',
                'Programming Language :: Python :: 3.5'])
    finally:
        del sys.path[0]
        os.chdir(old_path)

    return


if __name__ == '__main__':
    setup_package()