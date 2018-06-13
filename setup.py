from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy
ext_modules=[
    Extension("rc_cmd",
              sources=["cmds.pyx"],
              include_dirs=[numpy.get_include(),"."]
    )
]

setup(
  name = "rc",
  ext_modules = cythonize(ext_modules)
)