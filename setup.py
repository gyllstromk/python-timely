'''

Python Timely
=============

'''

from setuptools import setup
import os


setup(
    name='timely',
    version='0.1',
    url='https://github.com/gyllstromk/python-timely',
    license='BSD',
    author='Karl Gyllstrom',
    author_email='karl.gyllstrom+code@gmail.com',
    description='timely :: easy stopwatch interface in Python',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),

    py_modules=['timely'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[],

    tests_require=[],

    classifiers=[
    ],
    test_suite='test',
)
