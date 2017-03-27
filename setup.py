# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

exec(open('simpleplotly/version.py').read())


def main():
    setup(name='simpleplotly',
          version=__version__,
          author='ArrayStream',
          author_email='team@arraystream.com',
          url='https://github.com/arraystream/simpleplotly',
          description="simpleplotly makes generating charts with plotly easy",
          long_description=__doc__,
          classifiers=[
              'Development Status :: 4 - Beta',
              'Programming Language :: Python :: 3',
              'Programming Language :: Python :: 3.3',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Topic :: Scientific/Engineering :: Visualization',
          ],
          license='MIT',
          packages=find_packages(include=['simpleplotly']),
          install_requires=['plotly'],
          platforms='any')


if __name__ == '__main__':
    main()
