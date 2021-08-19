import sys
from setuptools import setup, find_packages, Extension
from numpy import get_include as get_np_include
from Cython.Build import cythonize


def main():
    include_dirs = [get_np_include()]
    define_macros = [('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')]

    extensions = [
        Extension('ts2vg.utils.pairqueue',
                  [f'ts2vg/utils/pairqueue.pyx']),

        Extension('ts2vg.graph._base',
                  [f'ts2vg/graph/_base.pyx'],
                  include_dirs=include_dirs,
                  define_macros=define_macros),

        Extension('ts2vg.graph._natural',
                  [f'ts2vg/graph/_natural.pyx'],
                  include_dirs=include_dirs,
                  define_macros=define_macros),

        Extension('ts2vg.graph._horizontal',
                  [f'ts2vg/graph/_horizontal.pyx'],
                  include_dirs=include_dirs,
                  define_macros=define_macros),
    ]
    
    extensions = cythonize(extensions)

    setup(ext_modules = extensions)

if __name__ == "__main__":
    main()
