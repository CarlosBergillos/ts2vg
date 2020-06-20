from setuptools import setup, Extension
from numpy import get_include as get_np_include

USE_CYTHON = False

def main():
    ext = 'pyx' if USE_CYTHON else 'c'
    
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()
        
        local_paths = ['src="./', '(./']
        absolute_root = "https://raw.githubusercontent.com/CarlosBergillos/ts2vg/master/"
        
        for lc in local_paths:
            long_description = long_description.replace(lc, lc[:-2] + absolute_root)
    
    include_dirs = [get_np_include()]
    define_macros = [("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]
        
    extensions = [
        Extension("ts2vg.nvg",
                  [f"ts2vg/nvg.{ext}"],
                  include_dirs=include_dirs,
                  define_macros=define_macros),
        Extension("ts2vg.pairqueue",
                  [f"ts2vg/pairqueue.{ext}"])
    ]
    
    if USE_CYTHON:
        from Cython.Build import cythonize
        extensions = cythonize(extensions)

    setup(
        name                = "ts2vg",
        version             = "0.1",
        author              = "Carlos Bergillos",
        author_email        = "c.bergillos.v@gmail.com",
        description         = "Obtain visibility graphs from time series data.",
        long_description    = long_description,
        long_description_content_type="text/markdown",
        keywords            = "graph,network,visibility,time,series",
        url                 = "https://github.com/CarlosBergillos/ts2vg",
        project_urls        = {
            "Documentation": "https://carlosbergillos.github.io/ts2vg",
            "Source Code": "https://github.com/CarlosBergillos/ts2vg"
        },
        license             = 'MIT',
        classifiers         = [
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Cython",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Operating System :: OS Independent",
            "Topic :: Scientific/Engineering :: Mathematics",
            "Development Status :: 4 - Beta",
            "Intended Audience :: Science/Research",
        ],
        install_requires    = ['numpy'],
        ext_modules         = extensions,
        #script_args        = ['build_ext'],
        #options            = {'build_ext':{'inplace':True, 'force':True}},
        zip_safe            = False,
        packages            = ['ts2vg'],
        entry_points        = {
            'console_scripts': ['ts2vg=ts2vg.cli:main']
        })

if __name__ == "__main__":
    main()
