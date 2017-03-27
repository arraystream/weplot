# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

exec(open('simpleplotly/version.py').read())


def main():
    setup(name='simpleplotly',
          version=__version__,
          author='ArrayStream (Yu Zheng, Ran Fan, Yongxin Yang)',
          author_email='team@arraystream.com',
          url='https://github.com/arraystream/simpleplotly',
          description='An easy to use plotly wrapper for python / jupyter notebooks',
          long_description='simpleplotly makes generating charts with plotly easy',
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
