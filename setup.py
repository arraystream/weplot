import sys

from setuptools import setup, find_packages

exec(open('weplot/version.py').read())


def check_python_version():
    if sys.version_info[:2] < (3, 4):
        print('Python 3.4 or newer is required. Python version detected: {}'.format(sys.version_info))
        sys.exit(-1)


def main():
    setup(name='weplot',
          version=__version__,
          author='ArrayStream (Yu Zheng, Ran Fan)',
          author_email='team@arraystream.com',
          url='https://github.com/arraystream/weplot',
          description='An easy to use plotly wrapper for python / jupyter notebooks',
          long_description='weplot makes generating charts with plotly easy',
          classifiers=[
              'Development Status :: 4 - Beta',
              'Programming Language :: Python :: 3',
              'Programming Language :: Python :: 3.3',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Topic :: Scientific/Engineering :: Visualization',
          ],
          license='MIT',
          packages=find_packages(include=['weplot']),
          install_requires=['plotly'],
          platforms='any')


if __name__ == '__main__':
    check_python_version()
    main()
