def configuration(parent_package='', top_path=None):
    import numpy
    from numpy.distutils.misc_util import Configuration

    config = Configuration('cylib', parent_package, top_path)
    config.add_extension('arnoldi',
                         sources=['arnoldi.c'],
                         include_dirs=[numpy.get_include()])
    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())