from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'main app',
  ext_modules = cythonize("*.pyx"),
)